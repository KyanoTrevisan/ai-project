# Import necessary libraries
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from sklearn.model_selection import train_test_split
import pandas as pd

# Load the CSV file containing image paths and labels
log_file = "key_log.csv"
df = pd.read_csv(log_file)
group_sizes = df.groupby('key').size()
print(group_sizes)
# Sample the same amount of images for each key
sampled_df = df.groupby('key').apply(lambda x: x.sample(n=min(group_sizes))).reset_index(drop=True)

# Split the sampled data into training and validation sets
train_df, val_df = train_test_split(sampled_df, test_size=0.3, random_state=42)

# Image dimensions
input_shape = (224, 224, 3)  

# Data augmentation
datagen = ImageDataGenerator(
    rescale=1./255,
    validation_split=0.2,
    rotation_range=0,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=False,
    fill_mode='nearest'
)

# Load and preprocess the training data with data augmentation
train_generator = datagen.flow_from_dataframe(
    train_df,
    x_col='image',
    y_col='key',
    target_size=(224, 224),
    batch_size=32,
    class_mode='sparse',  
    subset='training'
)

# Load and preprocess the validation data without data augmentation
validation_generator = datagen.flow_from_dataframe(
    val_df,
    x_col='image',
    y_col='key',
    target_size=(224, 224),
    batch_size=32,
    class_mode='sparse',
    subset='validation'
)

# Print label tags for indices
print("Label Tags for Indices in Training Generator:")
print(train_generator.class_indices)

# Define the CNN model
model = tf.keras.models.Sequential([
    tf.keras.layers.Conv2D(32, (3, 3), activation='relu', input_shape=input_shape),
    tf.keras.layers.MaxPooling2D((2, 2)),
    tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
    tf.keras.layers.MaxPooling2D((2, 2)),
    tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(32, activation='relu'),
    tf.keras.layers.Dense(3, activation='softmax')
])

# Compile the model
model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

# Train the model
history = model.fit(train_generator, epochs=20, validation_data=validation_generator)

# Save the model
model.save('model.h5')