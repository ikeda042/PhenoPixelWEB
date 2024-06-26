
import * as React from 'react';
import { DataGrid, GridColDef, GridRenderCellParams, } from '@mui/x-data-grid';
import { Stack, Typography } from '@mui/material';
import { useParams } from 'react-router-dom';
import { useEffect, useState } from 'react';
import { Button } from '@mui/material';
import { Box } from '@mui/system';
import Grid from '@mui/material/Unstable_Grid2';
import Link from '@mui/material/Link';
import { Link as RouterLink } from 'react-router-dom';
import { ScatterChart } from '@mui/x-charts/ScatterChart';
import { axisClasses } from '@mui/x-charts/ChartsAxis';
import { CircularProgress } from '@mui/material';
import { settings } from '../settings';

type RowData = {
    cell_id: string;
    label_experiment: string;
    manual_label: number;
    perimeter: number;
    area: number;
    [key: string]: string | number;
};

const otherSetting = {
    yAxis: [{ label: ' Area (px^2)' }],
    xAxis: [{ label: 'Perimeter (px)' }],
    grid: { horizontal: true },
    sx: {
        [`& .${axisClasses.left} .${axisClasses.label}`]: {
            transform: 'translateX(-30px)',
        },
    },
};





export default function Dbcontents() {
    const { filename } = useParams();
    const [rows, setRows] = useState<RowData[]>([]);
    const [cellIds, setCellIds] = useState<string[]>([]);
    const [isLoading, setIsLoading] = useState<boolean>(false);

    const handleExport = () => {
        const csvData = convertToCSV(rows);
        downloadCSV(csvData, `${filename}.csv`);
    };

    useEffect(() => {
        fetch(`${settings.url_prefix}/cellapi/cells/databases/${filename}`)
            .then(response => response.json())
            .then((data: RowData[]) => {
                const rowsWithIds = data.map((row: RowData) => ({ id: row.cell_id, ...row }));
                setRows(rowsWithIds);
                setCellIds(rowsWithIds.map(row => row.cell_id));
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

    const handleExportStats = async () => {
        setIsLoading(true);
        const queryString = cellIds.map(id => `cell_ids=${id}`).join('&');
        const url = `${settings.url_prefix}/cellapi/cells/${filename}/stats/csv?${queryString}`;

        const response = await fetch(url);
        const blob = await response.blob();
        const csvUrl = window.URL.createObjectURL(blob);

        const link = document.createElement('a');
        link.href = csvUrl;
        link.setAttribute('download', `${filename}_stats.csv`);
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        setIsLoading(false);
    };


    const columns: GridColDef[] = [
        {
            field: 'cell_id', headerName: 'Cell ID', width: 200, align: 'center', headerAlign: 'center',
            renderCell: (params: GridRenderCellParams) =>
                <Link href={`/dbcontents/${filename}/cell/${(params.value as string).split('.')[0]}`}>{(params.value as string).split('.')[0]}</Link>,
        },
        { field: 'label_experiment', headerName: 'Label Experiment', width: 200, align: 'center', headerAlign: 'center' },
        { field: 'manual_label', headerName: 'Manual Label', width: 200, align: 'center', headerAlign: 'center' },
        { field: 'perimeter', headerName: 'Perimeter (px)', width: 200, align: 'center', headerAlign: 'center' },
        { field: 'area', headerName: 'Area (px^2)', width: 200, align: 'center', headerAlign: 'center' }
    ];

    return (
        <div style={{ height: 700, width: '100%' }}>
            <Box display="flex" flexDirection="row" justifyContent="space-between" alignItems="center" margin={5}  >
                <Typography variant="h4" component="h2" gutterBottom>
                    {filename}
                </Typography>
                <Box>
                    <Button variant="contained" onClick={handleExportStats} style={{ marginRight: "5px", backgroundColor: 'black', color: 'white' }} >
                        統計をCSV出力
                    </Button>
                    <Button variant="contained" onClick={handleExport} style={{ marginRight: "5px", backgroundColor: 'black', color: 'white' }} >
                        表をCSV出力
                    </Button>
                    <Button variant="contained" component={RouterLink} to={`/dbcontents/${filename}/overview`} style={{ backgroundColor: 'black', color: 'white' }}>
                        Overview
                    </Button>
                </Box>
            </Box>

            {isLoading ? (
                <Box display="flex" justifyContent="center" alignItems="center" height="100%">
                    <Stack spacing={2} direction="column" alignItems="center">
                        <CircularProgress />
                        <Typography variant="h4" component="h2" gutterBottom>
                            統計データを出力中...
                        </Typography>
                    </Stack>
                </Box>
            ) : (
                <>   <Grid container spacing={4} margin={5}>
                    <ScatterChart
                        width={600}
                        height={400}
                        series={[
                            {
                                label: 'Perimeter vs Area',
                                data: rows.map((row) => ({ x: row.perimeter, y: row.area, id: row.cell_id })),
                            },
                        ]}
                        {...otherSetting}
                    />
                </Grid>
                    <Grid container spacing={4} margin={5}>
                        <DataGrid
                            rows={rows}
                            columns={columns}
                            autoHeight
                            pagination
                        />
                    </Grid>
                </>
            )}

        </div>
    );
}
