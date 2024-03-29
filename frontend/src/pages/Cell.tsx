
import * as React from 'react';
import { DataGrid, GridColDef } from '@mui/x-data-grid';
import Link from '@mui/material/Link';
import { Typography } from '@mui/material';
import { useParams } from 'react-router-dom';
import { useEffect, useState } from 'react';
import { Button } from '@mui/material';
import { Box } from '@mui/system';
import Grid from '@mui/material/Unstable_Grid2';
import SquareImage from '../components/Squareimage';


export default function Cell() {
    const { filename, cellId } = useParams<{ filename: string, cellId: string }>();
    const imageUrl = `http://10.32.17.15:8000/cellapi/cells/${filename}/cell/${cellId}/ph`;

    return (
        <div style={{ height: 700, width: '100%' }}>
            <Typography variant="h4" align="center" gutterBottom>
                Cell ID: {cellId}
            </Typography>
            <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '60vh' }}>
                <SquareImage imgSrc={imageUrl} size={400} />
            </Box>

        </div>

    );
}
