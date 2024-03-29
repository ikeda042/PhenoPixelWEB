
import * as React from 'react';
import { DataGrid, GridColDef } from '@mui/x-data-grid';
import Link from '@mui/material/Link';
import { Typography } from '@mui/material';
import { useParams } from 'react-router-dom';
import { useEffect, useState } from 'react';
import { Button } from '@mui/material';
import { Box } from '@mui/system';
import Grid from '@mui/material/Unstable_Grid2';


export default function Cell() {
    const { filename, cellId } = useParams<{ filename: string, cellId: string }>();
    return (
        <div style={{ height: 700, width: '100%' }}>
            {filename} {cellId}
        </div>
    );
}
