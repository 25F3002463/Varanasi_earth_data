import ee
import requests
import pandas as pd
import matplotlib.pyplot as plt

# Initialize Earth Engine
ee.Initialize(project='gen-lang-client-0680422241')

# Varanasi coordinates
varanasi = ee.Geometry.Point([82.9739, 25.3176])

# Sentinel-2 dataset
collection = (
    ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED')
    .filterBounds(varanasi)
    .filterDate('2025-01-01', '2025-12-31')
    .filter(
        ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 20)
    )
)

# Create satellite composite
image = collection.median()

# Calculate NDVI
ndvi = image.normalizedDifference(
    ['B8', 'B4']
).rename('NDVI')

# Extract NDVI statistics
stats = ndvi.reduceRegion(
    reducer=ee.Reducer.mean()
        .combine(ee.Reducer.min(), '', True)
        .combine(ee.Reducer.max(), '', True),
    geometry=varanasi.buffer(10000),
    scale=10,
    maxPixels=1e9
)

# Get results in Python
results = stats.getInfo()

print("\nVARANASI SATELLITE ANALYSIS")
print("---------------------------")

for key, value in results.items():
    print(key, ":", value)


# Convert results into DataFrame

df = pd.DataFrame(
    list(results.items()),
    columns=['Metric', 'NDVI_Value']
)

print("\nNDVI DATAFRAME")
print(df)

# Plot NDVI statistics

plt.figure(figsize=(8, 5))

plt.bar(
    df['Metric'],
    df['NDVI_Value']
)

plt.title("Varanasi Vegetation Analysis")
plt.xlabel("NDVI Metrics")
plt.ylabel("NDVI Value")

plt.show()

# Define study area
region = varanasi.buffer(10000)

# Generate RGB image
rgb = image.visualize(
    bands=['B4', 'B3', 'B2'],
    min=0,
    max=3000
)

# Generate NDVI heatmap
ndvi_visual = ndvi.visualize(
    min=-0.2,
    max=0.8,
    palette=['blue', 'white', 'yellow', 'green']
)

# Generate download URLs
rgb_url = rgb.getThumbURL({
    'region': region,
    'dimensions': 1024,
    'format': 'png'
})

ndvi_url = ndvi_visual.getThumbURL({
    'region': region,
    'dimensions': 1024,
    'format': 'png'
})

# Download images
for url, filename in [
    (rgb_url, 'varanasi_satellite.png'),
    (ndvi_url, 'varanasi_ndvi.png')
]:

    response = requests.get(url, timeout=120)
    response.raise_for_status()

    with open(filename, 'wb') as file:
        file.write(response.content)

    print(filename, 'downloaded successfully!')