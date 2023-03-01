import pandas as pd
import numpy as np
from fpdf import FPDF

class PDFFilter:
    def __init__(self, file_location):
        self.__file_location = file_location
        self.__list_filter = ["PendryBoot", "Outside B"]
        self.__type_filtered = [[' Depot', 'Last name', 'First name']]

    def read_file(self, loc):

        ## Read Lines of the file
        with open(loc, encoding='latin-1') as f:
            lines = f.readlines()

        return lines

    def split_columns_by_space(self, lines, list_filter, type_filtered):
        ## Split each column
        for i in range(len(lines)):
            lines[i] = lines[i].split('	')

            if len(lines[i][1]) == 2:
                lines[i][1] = lines[i][1][0] + '0' + lines[i][1][1]

            for item in list_filter:
                if item in lines[i][0]:
                    removed_columns = [lines[i][1], lines[i][3], lines[i][4], '', '', '', '']
                    type_filtered.append(removed_columns)
        
        return type_filtered

    def divide_to_two_columns(self, df):

        # Inserting the titles in the second column
        df[4][0] = "Depot"
        df[5][0] = "Last Name"
        df[6][0] = "First Name"

        j = 53
        error = 0
        count = 0

        while j < len(self.__type_filtered) and error == 0:

            # Trying to filter
            try:
                count_lines = 0
                for i in range(j, j+52):
                    df[4][i - 52] = df[0][i]
                    df[5][i - 52] = df[1][i]
                    df[6][i - 52] = df[2][i]
                    count_lines += 1
            except:
                print(df.to_string())
                error = 1
                

            count += 1
            df.drop(
                labels=range(j, j+count_lines),
                axis=0,
                inplace=True,
            )

            j += 104

        for i in range(1,count+1):
            line = pd.DataFrame({0:' Depot', 1:'Last name', 2:'First name', 3:None, 4:' Depot', 5:'Last name', 6:'First name'}, index=[0])
            df = pd.concat([df.iloc[:53*i], line, df.iloc[53*i:]]).reset_index(drop=True)

        return df

    def generate_pdf(self, df):

        # Margin
        m = 0 
        # Page width: Width of A4 is 210mm
        pw = 100 - 2 * m 
        # Cell height
        ch = 5
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font('Arial', '', 8)

        # pdf.cell(w=(pw/2), h=ch, txt="Cell 2a", border=1, ln=0)

        for i in range(len(df.index)):
            pdf.cell(w=(pw/7), h=ch, txt=str(df[0][i]), border=1, ln=0)
            pdf.cell(w=(2*pw/5), h=ch, txt=str(df[1][i]), border=1, ln=0)
            pdf.cell(w=(2*pw/5), h=ch, txt=str(df[2][i]), border=1, ln=0)
            pdf.cell(w=(pw/5), h=ch, txt="", border=0, ln=0)
            pdf.cell(w=(pw/7), h=ch, txt=str(df[4][i]), border=1, ln=0)
            pdf.cell(w=(2*pw/5), h=ch, txt=str(df[5][i]), border=1, ln=0)
            pdf.cell(w=(2*pw/5), h=ch, txt=str(df[6][i]), border=1, ln=1)

        pdf.output(f"./example.pdf", "F")
    
    def main(self):

        lines = self.read_file(self.__file_location)

        self.__type_filtered = self.split_columns_by_space(lines, self.__list_filter, self.__type_filtered)
                    
        self.__type_filtered.sort()

        # print(self.__type_filtered)

        df = pd.DataFrame(data= self.__type_filtered)

        df = self.divide_to_two_columns(df)

        self.generate_pdf(df)
