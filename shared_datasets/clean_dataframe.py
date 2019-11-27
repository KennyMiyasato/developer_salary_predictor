import pandas as pd


class CleanDataframe:
    columns = [
        'Respondent', 'ConvertedComp', 'WorkWeekHrs', 'YearsCode', 'Age',
        'OrgSize', 'Gender', 'Ethnicity', 'LanguageWorkedWith', 'Country',
        'Extraversion', 'Dependents', 'Trans', 'EdLevel', 'Student', 'MainBranch',
        'WorkLoc', 'WorkPlan', 'ImpSyn', 'Employment', 'CodeRevHrs',
        'OpSys', 'BetterLife', 'ResumeUpdate', 'YearsCodePro', 'LastHireDate', 'JobSat',
        'CareerSat', 'JobSeek', 'Hobbyist', 'CompFreq', 'SOVisitFreq', 'SOPartFreq', 'FizzBuzz'
    ]

    def __init__(self, df_of_csv_file=None):
        if df_of_csv_file is None:
            self.df_of_csv_file = None
        else:
            self.df_of_csv_file = df_of_csv_file

        self.cleaned_df = self.get_columns_from_raw_df()
        self.cleaned_df = self.add_continents_column_to_df(self.cleaned_df)
        self.cleaned_df = self.clean_df(self.cleaned_df)
        self.cleaned_df = self.create_dummies(self.cleaned_df)
        self.cleaned_df = self.dropnan_values(self.cleaned_df)
        self.cleaned_df = self.add_interactions(self.cleaned_df)

    def get_columns_from_raw_df(self):
        cleaned_df = self.df_of_csv_file[self.columns].dropna()
        return cleaned_df

    # def __repr__(self):
    #     return self.cleaned_df

    africa = [
        "Algeria", "Angola", "Benin",
        "Botswana", "Burkina Faso", "Burundi", "Cameroon",
        "Cape Verde", "Central African Republic", "Chad", "Comoros",
        "Republic of the Congo", "Democratic Republic of the Congo", "Congo, Republic of the...", "Côte d'Ivoire", "Djibouti",
        "Egypt", "Equatorial Guinea", "Eritrea", "Ethiopia",
        "Gabon", "The Gambia", "Ghana", "Guinea",
        "Guinea-Bissau", "Kenya", "Lesotho", "Liberia",
        "Libya", "Libyan Arab Jamahiriya", "Madagascar", "Malawi", "Mali",
        "Mauritania", "Mauritius", "Morocco", "Mozambique",
        "Namibia", "Niger", "Nigeria", "Rwanda",
        "São Tomé and Príncipe", "Senegal", "Seychelles", "Sierra Leone",
        "Somalia", "South Africa", "South Sudan", "Sudan",
        "Swaziland", "Tanzania", "United Republic of Tanzania", "Togo", "Tunisia",
        "Uganda", "Western Sahara", "Zambia", "Zimbabwe"
    ]

    asia = [
        "Afghanistan", "Armenia", "Azerbaijan", "Bahrain",
        "Bangladesh", "Bhutan", "Brunei", "Brunei Darussalam", "Cambodia",
        "China", "Cyprus", "East Timor", "Timor-Leste", "Georgia",
        "Hong Kong", "Hong Kong (S.A.R.)", "India", "Indonesia", "Iran",
        "Iraq", "Israel", "Japan", "Jordan",
        "Kazakhstan", "Kuwait", "Kyrgyzstan", "Laos", "Lao People's Democratic Republic",
        "Lebanon", "Malaysia", "Maldives", "Mongolia",
        "Myanmar", "Nepal", "North Korea", "Republic of Korea", "Oman",
        "Pakistan", "Palestine", "Philippines", "Qatar",
        "Russia", "Saudi Arabia", "Singapore", "South Korea",
        "Sri Lanka", "Syria", "Syrian Arab Republic", "Taiwan", "Tajikistan",
        "Thailand", "Turkey", "Turkmenistan", "United Arab Emirates",
        "Uzbekistan", "Vietnam", "Viet Nam", "Yemen"
    ]

    europe = [
        "Albania", "Andorra", "Austria", "Belarus",
        "Belgium", "Bosnia and Herzegovina", "Bulgaria", "Croatia",
        "Czech Republic", "Denmark", "Estonia", "Finland",
        "France", "Germany", "Greece", "Hungary",
        "Iceland", "Republic of Ireland", "Ireland", "Italy", "Kosovo ",
        "Latvia", "Liechtenstein", "Lithuania", "Luxembourg",
        "Macedonia", "The former Yugoslav Republic of Macedonia", "Republic of Moldova", "Monaco",
        "Malta", "Moldova", "Montenegro", "Netherlands", "Norway", "Poland",
        "Portugal", "Romania", "Russia", "Russian Federation", "San Marino",
        "Serbia", "Slovakia", "Slovenia", "Spain",
        "Sweden", "Switzerland", "Ukraine", "United Kingdom",
        "Vatican City "
    ]

    north_america = [
        "Antigua and Barbuda", "Anguilla", "Aruba", "The Bahamas",
        "Barbados", "Belize", "Bermuda", "Bonaire",
        "British Virgin Islands", "Canada", "Cayman Islands", "Clipperton Island",
        "Costa Rica", "Cuba", "Curaçao", "Dominica",
        "Dominican Republic", "El Salvador", "Greenland", "Grenada",
        "Guadeloupe", "Guatemala", "Haiti", "Honduras",
        "Jamaica", "Martinique", "Mexico", "Montserrat",
        "Navassa Island", "Nicaragua", "Panama", "Puerto Rico",
        "Saba", "Saint Barthelemy", "Saint Kitts and Nevis", "Saint Lucia",
        "Saint Martin", "Saint Pierre and Miquelon", "Saint Vincent and the Grenadines", "Sint Eustatius",
        "Sint Maarten", "Trinidad and Tobago", "Turks and Caicos", "United States",
        "US Virgin Islands"
    ]

    south_america = [
        "Argentina", "Bolivia", "Brazil", "Chile",
        "Colombia", "Ecuador", "French Guiana", "Guyana",
        "Paraguay", "Peru", "South Georgia and the South Sandwich Islands", "Suriname",
        "Uruguay", "Venezuela", "Venezuela, Bolivarian Republic of..."
    ]

    oceania_australia = [
        "Australia", "Federated States of Micronesia", "Fiji", "Kiribati",
        "Marshall Islands", "Nauru", "New Zealand", "Palau",
        "Papua New Guinea", "Samoa", "Solomon Islands", "Tonga",
        "Tuvalu", "Vanuatu"
    ]

    @staticmethod
    def GetConti(country):
        if country in CleanDataframe.africa:
            return "Africa"
        elif country in CleanDataframe.asia:
            return "Asia"
        elif country in CleanDataframe.europe:
            return "Europe"
        elif country in CleanDataframe.north_america:
            return "North America"
        elif country in CleanDataframe.south_america:
            return "South America"
        elif country in CleanDataframe.oceania_australia:
            return "Oceania Australia"
        else:
            return "None"

    def add_continents_column_to_df(self, cleaned_df):
        cleaned_df['Continent'] = self.cleaned_df['Country'].apply(
            lambda x: self.GetConti(x))
        clean_other = self.cleaned_df[self.cleaned_df['Continent']
                                      == 'None'].index
        self.cleaned_df.drop(clean_other, inplace=True)
        return cleaned_df

    def clean_df(self, cleaned_df):
        # Converting YearsCode to numberic instead of object
        cleaned_df = cleaned_df.replace(
            to_replace=["Less than 1 year", "More than 50 years"], value=["0", "50"])
        cleaned_df['YearsCode'] = pd.to_numeric(cleaned_df['YearsCode'])

        # Converting YearsCode to numberic instead of object
        cleaned_df['YearsCodePro'] = pd.to_numeric(cleaned_df['YearsCodePro'])

        # Separating LanguageWorkedWith, Ethnicity, Gender to be a list
        cleaned_df['LanguageWorkedWith'] = [
            x.split(sep=';') for x in cleaned_df['LanguageWorkedWith'].values]
        cleaned_df['Ethnicity'] = [x.split(sep=';')
                                   for x in cleaned_df['Ethnicity'].values]
        cleaned_df.loc[cleaned_df['Gender'].str.contains(
            ";"), 'Gender'] = 'Non-binary, genderqueer, or gender non-conforming'

        # Cleaning Age column
        df_age_calc = pd.DataFrame(
            cleaned_df[['Respondent', 'YearsCode', 'Age']])
        df_age_calc['learned_code'] = (
            cleaned_df['Age'] - cleaned_df['YearsCode'])
        less_than_18 = df_age_calc[df_age_calc['learned_code'] < 15].index
        less_over_65 = df_age_calc[df_age_calc['Age'] > 65].index
        df_age_calc.drop(less_than_18, inplace=True)
        df_age_calc.drop(less_over_65, inplace=True)
        df_age_calc = df_age_calc.drop(columns=['YearsCode', 'Age'])
        cleaned_df = cleaned_df.join(
            df_age_calc.set_index('Respondent'), on='Respondent')

        # Cleaning WorkWeekHrs
        over_100_hrs = cleaned_df[cleaned_df['WorkWeekHrs'] > 100].index
        cleaned_df.drop(over_100_hrs, inplace=True)

        # Cleaning ConvertedComp column
        troll = cleaned_df[cleaned_df['ConvertedComp'] > 500000].index
        cleaned_df.drop(troll, inplace=True)

        troll_1 = cleaned_df[cleaned_df['ConvertedComp'] < 1000].index
        cleaned_df.drop(troll_1, inplace=True)

        return cleaned_df

    def create_dummies(self, cleaned_df):
        df_language = pd.get_dummies(
            cleaned_df['LanguageWorkedWith'].apply(pd.Series).stack()).sum(level=0)
        df_language['LanguageWorkedWith_Total'] = df_language.sum(axis=1)

        df_ethnicity = pd.get_dummies(
            cleaned_df['Ethnicity'].apply(pd.Series).stack()).sum(level=0)

        cleaned_df = cleaned_df.join(df_language)
        cleaned_df = cleaned_df.join(df_ethnicity)

        cleaned_df = cleaned_df.drop(labels='LanguageWorkedWith', axis=1)
        cleaned_df = cleaned_df.drop(labels='Ethnicity', axis=1)

        cleaned_df = pd.get_dummies(cleaned_df)

        return cleaned_df

    def dropnan_values(self, cleaned_df):
        cleaned_df = self.cleaned_df.dropna()
        return cleaned_df

    @staticmethod
    def add_interaction(cleaned_df, column1, column2):
        cleaned_df['{}:{}'.format(column1, column2)] = cleaned_df.apply(
            lambda x: x[column1]*x[column2], axis=1)

    def add_interactions(self, cleaned_df):
        self.add_interaction(self.cleaned_df, 'Gender_Woman', 'Dependents_Yes')
        self.add_interaction(
            self.cleaned_df, 'White or of European descent', 'Gender_Man')

        ethnicities = [
            'Biracial', 'Black or of African descent', 'East Asian',
            'Hispanic or Latino/Latina', 'Middle Eastern', 'Multiracial',
            'Native American, Pacific Islander, or Indigenous Australian', 'South Asian'
        ]

        for ethnicity in ethnicities:
            self.add_interaction(cleaned_df, ethnicity, 'Gender_Woman')

        self.add_interaction(
            cleaned_df, 'ImpSyn_Far above average', 'Gender_Man')

        return cleaned_df
