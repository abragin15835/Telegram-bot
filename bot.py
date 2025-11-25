import telebot
import random
import os
from config import token
from logic import gen_pass
print('1')
from keras.models import load_model  # TensorFlow is required for Keras to work
print('2')
from PIL import Image, ImageOps  # Install pillow instead of PIL
print('3')
import numpy as np
print('4')

bot = telebot.TeleBot(token)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Я твой Telegram бот. Напиши что-нибудь!")

#@bot.message_handler(commands=['mem'])
#def send_mem(message):
    #img_name = random.choice(os.listdir('images'))
    #with open (f'images/{img_name}', 'rb') as f:
        #bot.send_photo(message.chat.id, f)

@bot.message_handler(commands=['username'])
def send_username(message):
    bot.reply_to(message, "Как тебя зовут?")
@bot.message_handler(commands=['andrei'])
def send_name(message):
    bot.reply_to(message, "Привет! Приятно познакомиться!")



    
@bot.message_handler(commands=['hello'])
def send_hello(message):
    bot.reply_to(message, "Привет! Как дела?")

@bot.message_handler(commands=['bye'])
def send_bye(message):
    bot.reply_to(message, "Пока! Удачи!")

@bot.message_handler(commands=['pass'])
def send_pass(message):
    bot.reply_to(message,gen_pass(10))

@bot.message_handler(commands=['iamsmart'])
def send_smart(message):
    bot.reply_to(message, "Да, я знаю")

@bot.message_handler(commands=['best_football_club'])
def send_club(message):
    bot.reply_to(message, "Спартак Москва")

@bot.message_handler(content_types=['photo'])
def message_photo(message):
    file_info = bot.get_file(message.photo[-1].file_id)
    file_name = file_info.file_path.split('/')[-1]
    downloaded_file = bot.download_file(file_info.file_path)
    bot.reply_to(message, 'Крутая картинка!')
    with open(file_name, 'wb') as new_file:
        new_file.write(downloaded_file)

    
    # Disable scientific notation for clarity
    np.set_printoptions(suppress=True)

    # Load the model
    model = load_model("keras_model.h5", compile=False)

    # Load the labels
    class_names = open("labels.txt", "r", encoding="UTF-8").readlines()

    # Create the array of the right shape to feed into the keras model
    # The 'length' or number of images you can put into the array is
    # determined by the first position in the shape tuple, in this case 1
    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

    # Replace this with the path to your image
    image = Image.open(file_name).convert("RGB")

    # resizing the image to be at least 224x224 and then cropping from the center
    size = (224, 224)
    image = ImageOps.fit(image, size, Image.Resampling.LANCZOS)

    # turn the image into a numpy array
    image_array = np.asarray(image)

    # Normalize the image
    normalized_image_array = (image_array.astype(np.float32) / 127.5) - 1

    # Load the image into the array
    data[0] = normalized_image_array

    # Predicts the model
    prediction = model.predict(data)
    index = np.argmax(prediction)
    class_name = class_names[index]
    confidence_score = prediction[0][index]

    # Print prediction and confidence score
    bot. reply_to (message, class_name [2:])
    print("Class:", class_name[2:], end="")
    print("Confidence Score:", confidence_score)


bot.polling()