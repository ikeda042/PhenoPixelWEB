import { Box } from '@mui/system';
import { DataGrid } from '@mui/x-data-grid';
import { useNavigate } from 'react-router-dom';

interface DBTableProps {
    data: { file_name: string; cell_count: number }[];
}

export default function DBtable({ data }: DBTableProps) {
    const navigate = useNavigate();

    const columns = [
        {
            field: 'file_name', headerName: 'File Name', width: 200
        },
        { field: 'cell_count', headerName: 'Cell Count', width: 200 },
        { field: 'antibiotics', headerName: 'Antibiotics', width: 200 },
        { field: 'exposure_time', headerName: 'Exposure time (min)', width: 200 },
        { field: 'strain_code', headerName: 'Strain code', width: 200 }
    ];

    return (
        <DataGrid
            rows={data.map((row, index) => {

                const matchResult = row.file_name.match(/tri(\d+)min/);
                const exposure_time = Number(matchResult?.[1] ?? 0);
                return {
                    id: index,
                    ...row,
                    antibiotics: row.file_name.includes('tri') ? 'Triclosan' : row.file_name,
                    exposure_time: exposure_time,
                    strain_code: Number(row.file_name.match(/\d+/)?.[0] ?? 0)
                };
            })}
            columns={columns}
            checkboxSelection
            disableRowSelectionOnClick
            hideFooterPagination
            onCellClick={(params, event) => {
                if (params.field === 'file_name') {
                    navigate(`/dbcontents/:${params.value}`);
                }
            }}
        />
    );
}
