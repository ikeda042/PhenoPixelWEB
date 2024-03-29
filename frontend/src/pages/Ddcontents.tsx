
import * as React from 'react';
import { DataGrid, GridColDef } from '@mui/x-data-grid';
import Link from '@mui/material/Link';
import { Typography } from '@mui/material';
import { useParams } from 'react-router-dom';

const columns: GridColDef[] = [
    { field: 'cell_id', headerName: 'Cell ID', width: 200, align: 'center', headerAlign: 'center' },
    { field: 'label_experiment', headerName: 'Label Experiment', width: 200, align: 'center', headerAlign: 'center' },
    { field: 'manual_label', headerName: 'Manual Label', width: 200, align: 'center', headerAlign: 'center' },
    { field: 'perimeter', headerName: 'Perimeter', width: 200, align: 'center', headerAlign: 'center' },
    { field: 'area', headerName: 'Area', width: 200, align: 'center', headerAlign: 'center' }
];


export default function Dbcontents() {
    const { filename } = useParams();
    const [rows, setRows] = React.useState([]);

    React.useEffect(() => {
        fetch(`/cells/databases/${filename}`)
            .then(response => response.json())
            .then(data => setRows(data));
    }, [filename]);

    return (
        <div style={{ height: 400, width: '100%' }}>
            <Link href="/">TOP</Link>
            <Typography variant="h4" component="h2" gutterBottom>
                {filename}
            </Typography>
            <DataGrid
                rows={rows}
                columns={columns}
                initialState={{
                    pagination: {
                        paginationModel: { page: 0, pageSize: 5 },
                    },
                }}
                pageSizeOptions={[5, 10]}
                checkboxSelection
            />
        </div>
    );
}
