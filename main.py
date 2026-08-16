import discord
from discord import app_commands
from discord.ext import commands

# --- KONFIGURACJA BOTA ---
TOKEN = "TWÓJ_TOKEN_BOTA"
GUILD_ID = 123456789012345678  # Zastąp numerem ID Twojego serwera (jako liczba)


class LSOBot(commands.Bot):

  def __init__(self):
    intents = discord.Intents.default()
    intents.message_content = True
    super().__init__(command_prefix="!", intents=intents)

  async def setup_hook(self):
    # Rejestracja komend Slash dla wybranego serwera (szybkie odświeżenie)
    guild = discord.Object(id=GUILD_ID)
    self.tree.copy_global_to(guild=guild)
    await self.tree.sync(guild=guild)
    print("✅ Komendy Slash zostały zsynchronizowane!")


bot = LSOBot()


# --- WIDOK PRZYCISKÓW DLA GRAFIKU ---
class GrafikButtons(discord.ui.View):

  def __init__(self):
    super().__init__(timeout=None)

  @discord.ui.button(
      label="Będę na służbie",
      style=discord.ButtonStyle.success,
      emoji="✅",
      custom_id="obecnosc_tak",
  )
  async def obecnosc_callback(
      self, interaction: discord.Interaction, button: discord.ui.Button
  ):
    await interaction.response.send_message(
        "✅ Twoja obecność została odnotowana!", ephemeral=True
    )

  @discord.ui.button(
      label="Szukam zastępstwa",
      style=discord.ButtonStyle.danger,
      emoji="🔄",
      custom_id="zastepstwo",
  )
  async def zastepstwo_callback(
      self, interaction: discord.Interaction, button: discord.ui.Button
  ):
    await interaction.response.send_message(
        "🔄 Zgłoszono poszukiwanie zastępstwa. Poinformuj również o tym na"
        " dedykowanym kanale!",
        ephemeral=True,
    )


# --- WIDOK PRZYCISKU DLA TICKETÓW ---
class TicketButton(discord.ui.View):

  def __init__(self):
    super().__init__(timeout=None)

  @discord.ui.button(
      label="Otwórz Zgłoszenie",
      style=discord.ButtonStyle.primary,
      emoji="📩",
      custom_id="open_ticket",
  )
  async def ticket_callback(
      self, interaction: discord.Interaction, button: discord.ui.Button
  ):
    await interaction.response.send_message(
        "📩 Twój ticket został utworzony. Opiekun wkrótce się z Tobą skontaktuje!",
        ephemeral=True,
    )


# --- ZDARZENIE URUCHOMIENIA ---
@bot.event
async def on_ready():
  print(f"✅ Bot LSO zalogowany jako {bot.user.name}")
  await bot.change_presence(
      activity=discord.Activity(
          type=discord.ActivityType.watching, name="Grafik LSO ⛪"
      )
  )


# --- KOMENDY SLASH ---


# 1. Komenda /grafik
@bot.tree.command(
    name="grafik", description="Wyświetla lub publikuje aktualny grafik służb LSO"
)
async def grafik(interaction: discord.Interaction):
  embed = discord.Embed(
      title="⛪ GRAFIK SŁUŻB LITURGICZNYCH",
      description="Aktualny grafik dyżurów i grup na ten tydzień:",
      color=discord.Color.blue(),
  )
  embed.add_field(
      name="📅 Sobota",
      value="**07:00** - Dyżurni\n**18:00** - Dyżurni",
      inline=False,
  )
  embed.add_field(
      name="☀️ Niedziela",
      value=(
          "**07:00** - Grupa A\n**10:30 & 12:00** - Grupa B / C\n**18:00** -"
          " Młodzież"
      ),
      inline=False,
  )
  embed.set_footer(
      text="Panel LSO • Aktualizacja", icon_url=bot.user.display_avatar.url
  )

  await interaction.response.send_message(
      embed=embed, view=GrafikButtons()
  )


# 2. Komenda /zbiorka
@bot.tree.command(name="zbiorka", description="Wysyła powiadomienie o zbiórce")
@app_commands.describe(
    data="Data i godzina zbiórki", opis="Opis lub temat zbiórki"
)
async def zbiorka(interaction: discord.Interaction, data: str, opis: str):
  embed = discord.Embed(
      title="🔔 ZBIÓRKA MINISTRANTÓW", color=discord.Color.gold()
  )
  embed.add_field(name="📅 Kiedy", value=data, inline=True)
  embed.add_field(name="📝 Temat / Opis", value=opis, inline=False)
  embed.set_footer(text="Obecność obowiązkowa!")

  await interaction.response.send_message(content="@everyone", embed=embed)


# 3. Komenda /ticket
@bot.tree.command(
    name="ticket",
    description="Tworzy panel zgłoszeniowy / ticket dla ministrantów",
)
async def ticket(interaction: discord.Interaction):
  embed = discord.Embed(
      title="🎫 Panel Zgłoszeń i Usprawiedliwień",
      description=(
          "Kliknij poniższy przycisk, aby otworzyć prywatne zgłoszenie do"
          " Zarządu/Opiekuna LSO (usprawiedliwienie, sprawa osobista, pytanie)."
      ),
      color=discord.Color.red(),
  )

  await interaction.response.send_message(embed=embed, view=TicketButton())


# --- URUCHOMIENIE BOTA ---
if __name__ == "__main__":
  bot.run(TOKEN)