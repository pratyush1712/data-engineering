"use client";
import { useState, ChangeEvent } from "react";
import * as XLSX from "xlsx";
import { ResultsDisplay } from "@/components";
import { ExcelData, ExcelRow } from "@/types";

export default function Home() {
  const [excelData, setExcelData] = useState<ExcelData>({});

  const handleFileUpload = (e: ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files![0];
    const reader = new FileReader();
    reader.onload = (evt) => {
      const bstr = evt?.target?.result as string;
      const wb: XLSX.WorkBook = XLSX.read(bstr, { type: "binary" });

      const allSheetData: ExcelData = {};
      wb.SheetNames.forEach((sheetName) => {
        const ws: XLSX.WorkSheet = wb.Sheets[sheetName];
        const data: ExcelRow[] = XLSX.utils.sheet_to_json(ws);
        allSheetData[sheetName] = data;
      });

      setExcelData(allSheetData);
    };
    reader.readAsBinaryString(file);
  };

  return (
    <main className="flex min-h-screen flex-col items-center justify-flex-start pt-12">
      <div className="relative py-6 w-full max-w-2xl text-center">
        <h1 className="relative z-10 text-sm sm:text-xl md:text-xl lg:text-xl font-bold">
          Welcome to the Data Collection and Analysis Platform for Cornell
          Innovations and Entrepreneurship (CI&E)
        </h1>
        <div className="absolute top-0 left-0 w-full h-full bg-white transform -skew-y-3 z-0"></div>
      </div>
      <div className="relative z-10 max-w-lg w-full text-center mt-8">
        <p className="mb-4 text-xl font-medium">
          Please upload the Excel sheet that contains all the companies whose
          data you want to fetch:
        </p>
        <input
          type="file"
          className="px-4 py-2 border border-gray-300 rounded-md shadow-sm text-base font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
          onChange={handleFileUpload}
        />
      </div>
      <div className="w-11/12 flex flex-col justify-center items-center">
        {/* <ResultsDisplay key={1} workbook={[]} /> */}
        {Object.entries(excelData).map((workbook, index) => (
          <ResultsDisplay
            key={index}
            category={workbook[0]}
            workbook={workbook[1]}
          />
        ))}
      </div>
    </main>
  );
}
