import discord
from discord.ext import commands
import pandas as pd
import requests
from PIL import Image, ImageDraw
from io import BytesIO

# Load the CSV data from the URL
csv_url = 'https://www.elsaleonie.com/python/wallpaper_MB.csv'
wallpaper_data = pd.read_csv(csv_url)

# Set your bot token
TOKEN = 'MTEwMzQyMzk5NDg1NTY5ODQ4Mw.GPmvFM.04olodOR20Qpt97UzGXXpYr4mqi5VcSDVPadr0'

# Enable all intents
intents = discord.Intents.all()

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.command(name='wallpaper')
async def generate_wallpaper(ctx, moonbats_token_id: int):
    # Find the row with the given token ID
    row = wallpaper_data.loc[wallpaper_data['id'] == moonbats_token_id]

    if not row.empty:
        ipfs_hash = row['ipfs_hash'].values[0]
        background_color = '#' + row['background'].values[0]

        # Fetch the image from the URL
        url = f'https://cloudflare-ipfs.com/ipfs/{ipfs_hash}'
        response = requests.get(url, timeout=5)
        fetched_image = Image.open(BytesIO(response.content))

        # Resize the fetched image
        resized_image = fetched_image.resize((1284, int(1284 * fetched_image.height / fetched_image.width)))

        # Create a new image with the desired size
        wallpaper = Image.new('RGB', (1284, 2778), background_color)

        # Paste the fetched image on the new image
        paste_x = (wallpaper.width - resized_image.width) // 2
        paste_y = 0
        wallpaper.paste(resized_image, (paste_x, paste_y))

        # Save the wallpaper to a buffer
        buffer = BytesIO()
        wallpaper.save(buffer, 'PNG')
        buffer.seek(0)

        # Send the wallpaper to the Discord channel
        await ctx.send(file=discord.File(fp=buffer, filename='wallpaper.png'))
    else:
        await ctx.send('Invalid Moonbats token ID. Please try again.')

# Run the bot
bot.run(TOKEN)
