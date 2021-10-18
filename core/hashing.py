from passlib.context import CryptContext

pwt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Hasher():

    @staticmethod
    def verifyPassword(plainPassword, hashedPassword):
        return pwt_context.verify(plainPassword, hashedPassword)

    @staticmethod
    def getHashedPassword(plainPassword):
        return pwt_context.hash(plainPassword)
