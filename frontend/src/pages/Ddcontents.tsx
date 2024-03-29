
import * as React from 'react';
import { DataGrid, GridColDef, GridRenderCellParams, } from '@mui/x-data-grid';
import { Typography } from '@mui/material';
import { useParams } from 'react-router-dom';
import { useEffect, useState } from 'react';
import { Button } from '@mui/material';
import { Box } from '@mui/system';
import Grid from '@mui/material/Unstable_Grid2';
import Link from '@mui/material/Link';


type RowData = {
    cell_id: string;
    label_experiment: string;
    manual_label: number;
    perimeter: number;
    area: number;
    [key: string]: string | number;
};




export default function Dbcontents() {
    const { filename } = useParams();
    const [rows, setRows] = useState<RowData[]>([]);

    const handleExport = () => {
        const csvData = convertToCSV(rows);
        downloadCSV(csvData, `${filename}.csv`);
    };

    useEffect(() => {
        fetch(`http://10.32.17.15:8000/cellapi/cells/databases/${filename}`)
            .then(response => response.json())
            .then((data: RowData[]) => {
                const rowsWithIds = data.map((row: RowData) => ({ id: row.cell_id, ...row }));
                setRows(rowsWithIds);
            });
    }, [filename]);

    const convertToCSV = (objArray: RowData[]): string => {
        const array = Array.isArray(objArray) ? objArray : JSON.parse(objArray);
        let str = `${columns.map(({ headerName }) => `"${headerName}"`).join(",")}\r\n`;

        return array.reduce((str: string, next: RowData) => {
            str += `${columns.map(({ field }) => `"${next[field]}"`).join(",")}\r\n`;
            return str;
        }, str);
    };

    const downloadCSV = (csvContent: string, fileName: string): void => {
        const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
        const link = document.createElement('a');
        link.href = URL.createObjectURL(blob);
        link.setAttribute('download', fileName);
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    };



    const columns: GridColDef[] = [
        {
            field: 'cell_id', headerName: 'Cell ID', width: 200, align: 'center', headerAlign: 'center',
            renderCell: (params: GridRenderCellParams) =>
                <Link href={`/dbcontents/${filename}/cell/${(params.value as string).split('.')[0]}`}>{(params.value as string).split('.')[0]}</Link>,
        },
        { field: 'label_experiment', headerName: 'Label Experiment', width: 200, align: 'center', headerAlign: 'center' },
        { field: 'manual_label', headerName: 'Manual Label', width: 200, align: 'center', headerAlign: 'center' },
        { field: 'perimeter', headerName: 'Perimeter (µm)', width: 200, align: 'center', headerAlign: 'center' },
        { field: 'area', headerName: 'Area (µm^2)', width: 200, align: 'center', headerAlign: 'center' }
    ];

    return (
        <div style={{ height: 700, width: '100%' }}>


            <Box display="flex" flexDirection="row" justifyContent="space-between" alignItems="center" margin={5}  >
                <Typography variant="h4" component="h2" gutterBottom>
                    {filename}
                </Typography>
                <Button variant="contained" onClick={handleExport} style={{ marginRight: "5px" }} >
                    CSV出力
                </Button>
            </Box>
            <Grid container spacing={4} margin={5}>
                <DataGrid
                    rows={rows}
                    columns={columns}
                    hideFooterPagination
                />
            </Grid>
        </div>
    );
}
