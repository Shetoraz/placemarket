class Announcement():

    def __init__(self, result):
        self.category = result[0]
        self.city = result[1]
        self.title = result[2]
        self.description = result[3]
        self.price = result[4]
        self.photo = result[5]
        self.contacts = result[6]

    def showInfo(self):
        info = "📝*{}*\n\n{}\n\n*Категория*: {}\n\n🇧🇾*Город*: {}\n\n💰*Цена*: {} BYN\n\n📞*Контакты*: {}".format(
            self.title, self.description, self.category, self.city, self.price, self.contacts)
        return info
