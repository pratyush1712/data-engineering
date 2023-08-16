import React, { useEffect, useState } from 'react';
import axios, { CancelTokenSource } from 'axios';
import { CompanyData, DataType } from '@/types';
import DataList from './DataList';

interface Props {
    category: string;
    workbook: CompanyData[];
}

type Companies = Record<string, CompanyData>;

const MainComponent: React.FC<Props> = ({ category, workbook }) => {
    const [companies, setCompanies] = useState<Companies>({});
    const [duns, setDuns] = useState<CompanyData[]>([]);
    const [ein, setEin] = useState<CompanyData[]>([]);
    const [ticker, setTicker] = useState<CompanyData[]>([]);

    useEffect(() => {
        let cancelSource: CancelTokenSource;

        const fetchData = async () => {
            try {
                const response = await fetch('http://localhost:5001/api/companies', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ companies: workbook })
                });

                const reader = response.body!.pipeThrough(new TextDecoderStream()).getReader();

                while (true) {
                    const { value, done } = await reader.read();
                    if (done) break;
                    const data = JSON.parse(value);
                    if (data['D-U-N-S'] && (!companies[data.Company] || !companies[data.Company]['D-U-N-S'])) {
                        setDuns((duns) => [...duns, data]);
                    } else if (data.EIN && (!companies[data.Company] || !companies[data.Company].EIN)) {
                        setEin((ein) => [...ein, data]);
                    } else if (data.Ticker && (!companies[data.Company] || !companies[data.Company].Ticker)) {
                        setTicker((ticker) => [...ticker, data]);
                    }
                    setCompanies((companies) => ({ ...companies, [data.Company]: data }));
                }
            } catch (error) {
                if (axios.isCancel(error)) console.log('Request cancelled');
                else console.error('An error occurred: ', error);
            }
        };

        fetchData();

        return () => {
            if (cancelSource) {
                cancelSource.cancel('Component unmounted');
            }
        };
    }, [workbook]);

    return (
        <div className="flex flex-col text-start items-start bg-gray-200 w-10/12 overflow-x-scroll scrollbar-hide p-6 m-3">
            <h1 className="text-3xl text-gray-800 font-bold mt-6">{category}</h1>
            <div className="flex space-x-32 h-64 mt-4 align-self-center">
                <div className="flex flex-col items-stretch space-y-4 min-w-max overflow-auto">
                    <h2 className="mb-4 text-2xl text-gray-800">EIN Data</h2>
                    <DataList data={ein} dataType="EIN" />
                </div>
                <div className="flex flex-col items-stretch space-y-4 min-w-max overflow-auto">
                    <h2 className="mb-4 text-2xl text-gray-800">DUNS Data</h2>
                    <DataList data={duns} dataType="D-U-N-S" />
                </div>
                <div className="flex flex-col items-stretch space-y-4 min-w-max overflow-auto">
                    <h2 className="mb-4 text-2xl text-gray-800">Ticker Data</h2>
                    <DataList data={ticker} dataType="Ticker" />
                </div>
            </div>
        </div>
    );
};

export default MainComponent;
