export type CompanyData = {
    Company: string;
    EIN?: string | null;
    'D-U-N-S'?: string | null;
    'Primary Location'?: string | null;
    'D-U-N-S Company'?: string | null;
    'EIN Company'?: string | null;
    Ticker?: string | null;
    'Ticker Company'?: string | null;
};

export type DataType = 'EIN' | 'D-U-N-S' | 'Ticker';
