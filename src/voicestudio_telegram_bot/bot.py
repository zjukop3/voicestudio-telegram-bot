#!/usr/bin/env python3
"""Main Telegram bot implementation for VoiceStudio."""
import os
import logging
import tempfile
from pathlib import Path

import requests
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
)

# Load environment variables from .env file (if present)
load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
VOICESTUDIO_API = os.getenv("VOICESTUDIO_API", "http://localhost:5000/api")

if not TELEGRAM_TOKEN:
    raise ValueError("TELEGRAM_TOKEN environment variable is required.")

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

# Store per-user cloned voice references (in memory for demo; use DB in production)
user_voices: dict[int, str] = {}  # user_id -> voice_id or file path


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a welcome message when /start is issued."""
    user = update.effective_user
    await update.message.reply_html(
        f"Hi {user.mention_html()}! I'm the VoiceStudio Telegram bot.\n\n"
        "Send me a text message and I'll read it aloud using VoiceStudio.\n"
        "Send me a voice message (sample) and I'll clone the speaker's voice for you.\n\n"
        "Use /help to see more options."
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a help message when /help is issued."""
    await update.message.reply_text(
        "🤖 VoiceStudio Bot Help\n\n"
        "/start - Start the bot\n"
        "/help  - Show this help\n"
        "/voice - Reset to default voice\n"
        "Send any text to generate speech.\n"
        "Send a voice message to clone a voice."
    )


async def reset_voice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Reset to default VoiceStudio voice."""
    user_id = update.effective_user.id
    user_voices.pop(user_id, None)
    await update.message.reply_text("🔊 Reset to default voice.")


async def handle_voice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Process a voice message for voice cloning."""
    user_id = update.effective_user.id
    voice_file = update.message.voice or update.message.audio
    if not voice_file:
        await update.message.reply_text("Please send a proper voice/audio message.")
        return

    # Download the voice sample from Telegram
    tg_file = await context.bot.get_file(voice_file.file_id)
    with tempfile.NamedTemporaryFile(suffix=".ogg", delete=False) as tmp:
        await tg_file.download_to_drive(tmp.name)
        sample_path = tmp.name
        logger.info(f"Downloaded voice sample to {sample_path}")

    try:
        # Send to VoiceStudio API to create a voice clone
        with open(sample_path, "rb") as f:
            files = {"audio": (Path(sample_path).name, f)}
            resp = requests.post(
                f"{VOICESTUDIO_API}/clone",
                files=files,
                data={"user_id": str(user_id)},
                timeout=30,
            )
        resp.raise_for_status()
        clone_result = resp.json()
        voice_id = clone_result.get("voice_id")
        if not voice_id:
            raise ValueError("No voice_id in clone response")

        # Store the clone for this user
        user_voices[user_id] = voice_id
        await update.message.reply_text(
            f"🎉 Voice cloned successfully! ID: `{voice_id}`. Now send me any text.",
            parse_mode="Markdown",
        )
    except Exception as e:
        logger.exception("Voice cloning failed")
        await update.message.reply_text(f"❌ Voice cloning failed: {e}")
    finally:
        # Clean up the temporary file
        os.unlink(sample_path)


async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Convert text to speech using VoiceStudio."""
    user_id = update.effective_user.id
    text = update.message.text
    if not text.strip():
        await update.message.reply_text("Please send non‑empty text.")
        return

    # Build TTS request payload
    payload = {"text": text}
    
    # If user has a cloned voice, attach it
    custom_voice = user_voices.get(user_id)
    if custom_voice:
        payload["voice_id"] = custom_voice

    try:
        resp = requests.post(
            f"{VOICESTUDIO_API}/tts",
            json=payload,
            timeout=30,
        )
        resp.raise_for_status()

        # Save the received audio to a temporary file, then send it
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
            tmp.write(resp.content)
            audio_path = tmp.name

        await context.bot.send_voice(
            chat_id=update.effective_chat.id,
            voice=open(audio_path, "rb"),
        )
        os.unlink(audio_path)  # clean up
    except requests.exceptions.RequestException as e:
        logger.error(f"TTS request failed: {e}")
        await update.message.reply_text(
            "⚠️ Could not generate speech. Is VoiceStudio service running?"
        )


def main() -> None:
    """Start the bot."""
    logger.info("Starting VoiceStudio Telegram bot...")
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    # Register handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("voice", reset_voice))
    application.add_handler(MessageHandler(filters.VOICE | filters.AUDIO, handle_voice))
    application.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text)
    )

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
