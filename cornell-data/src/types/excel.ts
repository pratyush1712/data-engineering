import { CompanyData } from './company';

export type ExcelRow = CompanyData;

export type ExcelData = { [sheetName: string]: ExcelRow[] };
