import os

print(os.environ.get("DATABASE_URL"))

os.environ['DATABASE_URL']='postgres://kkyceuncyvjkxe:b1b3ee8a9abc4efccab51570abf6888e48ff80d6570781338d6bdc1d8999cc57@ec2-52-202-66-191.compute-1.amazonaws.com:5432/dccmmcosuglg9u'
print( "Database_URL is " + str(os.environ['DATABASE_URL']))

