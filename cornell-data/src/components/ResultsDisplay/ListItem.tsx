import React from 'react';
import { CompanyData, DataType } from '@/types';

interface ListItemProps {
    item: CompanyData;
    dataType: DataType;
}

const ListItem: React.FC<ListItemProps> = ({ item, dataType }) => (
    <div
        className="p-4 bg-white min-w-max border border-gray-300 rounded shadow-sm cursor-pointer
    text-gray-800 hover:bg-gray-50 transition-all duration-200 ease-in-out 
    focus:outline-none focus:ring-2 focus:ring-indigo-500"
    >
        <h5 className="text-xl">
            <strong>Company: </strong> {item['Company']}
        </h5>
        <h5 className="text-xl">
            <strong>{dataType}: </strong> {item[dataType]}
        </h5>
    </div>
);

export default ListItem;
