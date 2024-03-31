import { Box } from '@mui/system';
import { DataGrid } from '@mui/x-data-grid';
import { GridRenderCellParams, GridColDef } from '@mui/x-data-grid';
import Link from '@mui/material/Link';
import Button from '@mui/material/Button';

interface DBTableProps {
    data: { file_name: string; cell_count: number }[];
}

export default function DBtable({ data }: DBTableProps) {

    const columns: GridColDef[] = [
        {
            field: 'file_name',
            headerName: 'Database name',
            width: 140,
            align: 'left',
            headerAlign: 'center',
            renderCell: (params: GridRenderCellParams) =>
                <Link href={`/dbcontents/${(params.value as string).split('.')[0]}`}>{(params.value as string).split('.')[0]}</Link>,
        },
        { field: 'cell_count', headerName: 'Cell Count', width: 200, align: 'center', headerAlign: 'center' },
        { field: 'antibiotics', headerName: 'Antibiotics', width: 200, align: 'center', headerAlign: 'center' },
        { field: 'exposure_time', headerName: 'Exposure time (min)', width: 200, align: 'center', headerAlign: 'center' },
        { field: 'strain_code', headerName: 'Strain code', width: 200, align: 'center', headerAlign: 'center' },
        {
            field: 'action',
            headerName: 'Export database',
            width: 150,
            align: 'center',
            headerAlign: 'center',
            renderCell: (params: GridRenderCellParams) => (
                <Button
                    variant="contained"
                    style={{ backgroundColor: 'black', color: 'white' }}
                    onClick={() => {
                        const dbName = (params.row.file_name as string).split('.')[0];
                        window.open(`http://10.32.17.15:8000/cellapi/cells/databases/${dbName}/sqliteexport`, '_blank');
                    }}
                >
                    Export
                </Button>
            ),
        },
    ];


    return (
        <DataGrid
            rows={data.map((row, index) => {
                const matchResult = row.file_name.match(/[a-z]{3}(\d+)min/);
                const exposure_time = Number(matchResult?.[1] ?? 0);
                return {
                    id: index,
                    ...row,
                    antibiotics: row.file_name.includes('tri') ? 'Triclosan'
                        : row.file_name.includes('cip') ? 'Ciprofloxacin'
                            : row.file_name.includes('gen') ? 'Gentamicin'
                                : row.file_name.includes('amp') ? 'Ampicillin'
                                    : row.file_name,
                    exposure_time: exposure_time,
                    strain_code: row.file_name.includes('pi') ? 'PI' : Number(row.file_name.match(/\d+/)?.[0] ?? 0)
                };
            })}
            columns={columns}
            disableRowSelectionOnClick
            hideFooterPagination
        />
    );
}
