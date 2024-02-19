##################################### Rule_Based_Classification ####################################


# Ein Spieleunternehmen plant, neue Kundendefinitionen (Personas) basierend auf verschiedenen Kundenmerkmalen wie
# Land, Quelle, Alter und Geschlecht zu erstellen. Ziel ist es, diese neuen Kundendefinitionen zu verwenden, um
# Kundensegmente zu erstellen und abzuschätzen, wie viel Gewinn mit den neuen Kunden in diesen Segmenten generiert
# werden kann.

# In dieser Studie wird schrittweise erläutert, wie eine regelbasierte Klassifizierung und die Berechnung der
# kundenbasierten Einnahmen durchgeführt werden.


########################## Importieren von Bibliotheken ##########################


import pandas as pd

pd.set_option("display.max_columns", None)
pd.set_option("display.width", 500)
pd.set_option("display.max_rows", None)
pd.set_option("display.float_format", lambda x: "%.3f" % x)
pd.set_option("display.expand_frame_repr", True)



############################################ Abrufen der Daten ##################################

df = pd.read_csv("datasets/persona.csv")
df.head()



########################################### Beschreibung der Daten ###############################

def check_df(dataframe):
    print(f"""
    ########################## Shape #########################\n\n{dataframe.shape}\n\n
    ########################## Types #########################\n\n{dataframe.dtypes}\n\n
    ########################## Head  #########################\n\n{dataframe.head(3)}\n\n
    ########################## NA    #########################\n\n{dataframe.isnull().sum()}\n\n
    ########################## Quantiles #####################\n\n{dataframe.describe([0, 0.05, 0.50, 0.95, 0.99, 1]).T}\n\n""")




check_df(df)



########################################### Datenanalyse ###################################

def data_analysis(dataframe):
    # Unique Werte von Source:
    print("Unique Values of Source:\n", dataframe[["SOURCE"]].nunique())

    # Häufigkeit der Source:
    print("Frequency of Source:\n", dataframe[["SOURCE"]].value_counts())

    # Unique Werte von Price:
    print("Unique Values of Price:\n", dataframe[["PRICE"]].nunique())

    # Anzahl der Produktverkäufe nach Verkaufspreis:
    print("Number of product sales by sales price:\n", dataframe[["PRICE"]].value_counts())

    # Anzahl der Produktverkäufe nach Land:
    print("Number of product sales by sales by country:\n", dataframe["COUNTRY"].value_counts(ascending=False, normalize=True))

    # Gesamt- und Durchschnittsbetrag der Verkäufe nach Land:
    print("Total & average amount of sales by country:\n", dataframe.groupby("COUNTRY").agg({"PRICE": ["mean", "sum"]}))

    # Durchschnittlicher Verkaufsbetrag nach Source:
    print("Average amount of sales by source:\n", dataframe.groupby("SOURCE").agg({"PRICE": "mean"}))

    # Durchschnittlicher Verkaufsbetrag nach Source und Country:
    print("Average amount of sales by source and country:\n", dataframe.pivot_table(values=["PRICE"],
                                                                                    index=["COUNTRY"],
                                                                                    columns=["SOURCE"],
                                                                                    aggfunc=["mean"]))



data_analysis(df)



########################################## Definition von Personas ###############################



def define_persona(dataframe):
    # Zuerst wandeln wir das Alter in kategorische Daten um und definieren dann neue Kundenprofile (Personas) anhand von
    # Country, Source, Age Und Sex.

    bins = [dataframe["AGE"].min(), 18, 23, 35, 45, dataframe["AGE"].max()]
    labels = [str(dataframe["AGE"].min()) + "_18", "19_23", "24_35", "36_45", "46_" + str(dataframe["AGE"].max())]

    dataframe["AGE_CAT"] = pd.cut(dataframe["AGE"], bins, labels=labels)
    dataframe.groupby("AGE_CAT").agg({"AGE": ["min", "max", "count"]})

    # Um Personas zu erstellen, gruppieren wir alle Merkmale im Datensatz:
    df_summary = dataframe.groupby(["COUNTRY", "SOURCE", "SEX", "AGE_CAT"])[["PRICE"]].sum().reset_index()
    df_summary["CUSTOMERS_LEVEL_BASED"] = pd.DataFrame(["_".join(row).upper() for row in df_summary.values[:, 0:4]])

    # Berechnung des durchschnittlichen Betrags der Personas:
    df_persona = df_summary.groupby("CUSTOMERS_LEVEL_BASED").agg({"PRICE": "mean"})
    df_persona = df_persona.reset_index()

    return df_persona



define_persona(df)


######################################### Erstellen von Segmenten basierend auf Personas ###############


def create_segments(dataframe):
    # Beim Auflisten der Preise in absteigender Reihenfolge kennzeichnen wir das beste Segment als A-Segment und
    # definieren insgesamt vier Segmente.

    df_persona = define_persona(dataframe)

    segment_labels = ["D", "C", "B", "A"]
    df_persona["SEGMENT"] = pd.qcut(df_persona["PRICE"], 4, labels=segment_labels)
    # df_segment = df_persona.groupby("SEGMENT").agg({"PRICE": "mean"})

    return df_persona



create_segments(df)



####################################### Prädiktion  ########################################

def ruled_based_classification(dataframe):
    df_segment = create_segments(dataframe)

    def get_age_category(age):
        age_ranges = [(18, "13_18"), (23, "19_23"), (35, "24_35"), (45, "36_45"), (70, "46_70")]
        return next((category for upper, category in age_ranges if age <= upper), "UNKNOWN")

    COUNTRY = input("Enter a country name (USA/ CAN/ TUR/ DEU/ FRA/ BRA):")
    SOURCE = input("Enter the operating system of phone (IOS/ ANDROID):")
    SEX = input("Enter the gender (FEMALE/ MALE):")
    AGE = int(input("Enter the age:"))
    AGE_SEG = get_age_category(AGE)
    new_user = COUNTRY.upper() + "_" + SOURCE.upper() + "_" + SEX.upper() + "_" + AGE_SEG


    print(new_user)
    segment = df_segment[df_segment["CUSTOMERS_LEVEL_BASED"] == new_user].loc[:, "SEGMENT"].values
    price = df_segment[df_segment["CUSTOMERS_LEVEL_BASED"] == new_user].loc[:, "PRICE"].values

    if segment:
        print("Segment:", segment[0])
    else:
        print("No segment found for this user.")
    if price:
        print("PRICE:", price[0])
    else:
        print("No price found for this user.")

    return new_user


ruled_based_classification(df)