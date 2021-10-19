import nextcord

class Confirm(nextcord.ui.View):
    def __init__(self):
        super().__init__()
        self.value = None

    @nextcord.ui.button(label=f'Send Message', style=nextcord.ButtonStyle.green, row = 0)
    async def yes(self,button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await interaction.response.defer(ephemeral = True)
        self.value= True
        self.stop()

    @nextcord.ui.button(label='Cancel Message', style=nextcord.ButtonStyle.red, row = 0)
    async def no(self,button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await interaction.response.defer(ephemeral = True)
        self.value= False
        self.stop()


