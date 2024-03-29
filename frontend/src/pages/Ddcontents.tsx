
import * as React from 'react';
import { DataGrid, GridColDef } from '@mui/x-data-grid';
import Link from '@mui/material/Link';
import { Typography } from '@mui/material';
import { useParams } from 'react-router-dom';
import { useEffect, useState } from 'react';
import { Button } from '@mui/material';


const convertToCSV = (objArray: RowData[]): string => {
    const array = Array.isArray(objArray) ? objArray : JSON.parse(objArray);
    let str = `${Object.keys(array[0]).map(value => `"${value}"`).join(",")}\r\n`;

    return array.reduce((str: string, next: RowData) => {
        str += `${Object.values(next).map(value => `"${value}"`).join(",")}\r\n`;
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

type RowData = {
    cell_id: string;
    label_experiment: string;
    manual_label: number;
    perimeter: number;
    area: number;
};



const columns: GridColDef[] = [
    { field: 'cell_id', headerName: 'Cell ID', width: 200, align: 'center', headerAlign: 'center' },
    { field: 'label_experiment', headerName: 'Label Experiment', width: 200, align: 'center', headerAlign: 'center' },
    { field: 'manual_label', headerName: 'Manual Label', width: 200, align: 'center', headerAlign: 'center' },
    { field: 'perimeter (µm)', headerName: 'Perimeter(µm)', width: 200, align: 'center', headerAlign: 'center' },
    { field: 'area (µm^2)', headerName: 'Area (µm^2)', width: 200, align: 'center', headerAlign: 'center' }
];


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

    return (

        <div style={{ height: 700, width: '100%' }}>
            <Link href="/">TOP</Link>
            <Typography variant="h4" component="h2" gutterBottom>
                {filename}
            </Typography>
            <Button variant="contained" onClick={handleExport} style={{ marginBottom: '10px' }}>
                Export to CSV
            </Button>
            <DataGrid
                rows={rows}
                columns={columns}
                hideFooterPagination
            />
        </div>
    );
}
