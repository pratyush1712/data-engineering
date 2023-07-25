import ListItem from './ListItem';
import { CompanyData, DataType } from '@/types';

interface DataListProps {
    data: CompanyData[];
    dataType: DataType;
}

const DataList: React.FC<DataListProps> = ({ data, dataType }) => (
    <div className="flex flex-col space-y-4 overflow-y-auto scrollbar-hide text-start">
        {data.map((item, index) => (
            <ListItem key={index} item={item} dataType={dataType} />
        ))}
    </div>
);

export default DataList;
