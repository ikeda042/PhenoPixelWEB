import { Box } from '@mui/system';
import { DataGrid } from '@mui/x-data-grid';
import { GridRenderCellParams, GridColDef } from '@mui/x-data-grid';
import Link from '@mui/material/Link';

interface DBTableProps {
    data: { file_name: string; cell_count: number }[];
}

export default function DBtable({ data }: DBTableProps) {

    const columns: GridColDef[] = [
        {
            field: 'file_name',
            headerName: 'Database name',
            width: 250,
            align: 'center',
            headerAlign: 'center',
            renderCell: (params: GridRenderCellParams) =>
                <Link href={`/dbcontents/${(params.value as string).split('.')[0]}`}>{(params.value as string).split('.')[0]}</Link>,

        },
        { field: 'cell_count', headerName: 'Cell Count', width: 200, align: 'center', headerAlign: 'center' },
        { field: 'antibiotics', headerName: 'Antibiotics', width: 200, align: 'center', headerAlign: 'center' },
        { field: 'exposure_time', headerName: 'Exposure time (min)', width: 200, align: 'center', headerAlign: 'center' },
        { field: 'strain_code', headerName: 'Strain code', width: 200, align: 'center', headerAlign: 'center' }
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
            disableRowSelectionOnClick
            hideFooterPagination
        />
    );
}
