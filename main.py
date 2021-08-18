from app.bot import Bot
from cogs.admin import Admin
from cogs.utils import Utils


kita = Bot()

kita.add_cog(Admin(kita))
kita.add_cog(Utils(kita))

kita.run()
