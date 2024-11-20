import pandas as pd


def main():
    # File path to the JSON file
    file_path = "house_data.json"  # Replace with the path to your JSON file

    # Read the JSON file
    try:
        df = pd.read_json(file_path, lines=False)
    except ValueError:
        print("Error reading JSON file. Please ensure it's properly formatted.")
        return

    # Drop duplicate records
    df_cleaned = df.drop_duplicates(
        subset=[
            "House_ID",
            "Listing_URL",
            "Address",
            "Tenure",
            "Beds",
            "Baths",
            "Receptions",
            "Price",
        ]
    )

    # Clean the Price column by removing currency symbols and commas, then convert to numeric
    df_cleaned["Price"] = (
        df_cleaned["Price"].replace({"[£$,]": ""}, regex=True).astype(float)
    )

    # Clean the Receptions column, converting "N/A" to None and other values to integers
    df_cleaned["Receptions"] = pd.to_numeric(df_cleaned["Receptions"], errors="coerce")

    # Extract the postal code from the address
    df_cleaned["Postal_Code"] = df_cleaned["Address"].str.extract(
        r"([A-Z]{1,2}\d{1,2}[A-Z]?\s?\d[A-Z]{2}|[A-Z]{1,2}\d[A-Z]?)"
    )

    # Save cleaned data to a CSV file
    output_path = "real_estate_cleaned.csv"
    df_cleaned.to_csv(output_path, index=False)
    print(f"Cleaned data saved to {output_path}")

    # Perform analysis: Average price by postal code (rounded to 4 decimal places)
    avg_price_by_postal = (
        df_cleaned.groupby("Postal_Code")["Price"]
        .mean()
        .reset_index()
        .rename(columns={"Price": "Avg_Price"})
    )
    avg_price_by_postal["Avg_Price"] = avg_price_by_postal["Avg_Price"].round(
        4
    )  # Round to 4 decimal places

    # Ensure pandas displays floats in standard format
    pd.options.display.float_format = "{:.4f}".format

    print("Average Price by Postal Code:")
    print(avg_price_by_postal)

    # Perform analysis: Distribution of properties by the number of bedrooms
    bedroom_distribution = (
        df_cleaned["Beds"]
        .value_counts()
        .reset_index()
        .rename(columns={"index": "Beds", "Beds": "Number_of_Properties"})
    )
    print("Distribution of Properties by Bedrooms:")
    print(bedroom_distribution)


if __name__ == "__main__":
    main()


# 𝗖𝗵𝗮𝘁𝗚𝗣𝗧 4.0 𝗣𝗟𝗨𝗦
# ✉️ ：evekano4257@outlook.com
# 🔑： 0fnt1Hp7X3Nv9Lt1
