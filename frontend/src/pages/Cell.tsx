
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
import { ToggleButton, ToggleButtonGroup } from '@mui/material';
import { Stack } from '@mui/material';

export default function Cell() {
    const { filename, cellId } = useParams<{ filename: string, cellId: string }>();
    const [view, setView] = React.useState('ph');

    const handleView = (event: React.MouseEvent<HTMLElement>, newView: string) => {
        setView(newView);
    };

    const imageUrl = `http://10.32.17.15:8000/cellapi/cells/${filename}/cell/${cellId}/${view}`;

    return (
        <div style={{ height: 700, width: '100%' }}>
            <Typography variant="h4" align="center" gutterBottom>
                Cell ID: {cellId}
            </Typography>

            <Box sx={{ display: 'flex', flexDirection: 'column-reverse', justifyContent: 'center', alignItems: 'center', height: '60vh' }}>

                <Stack direction="row" spacing={3}>
                    <ToggleButtonGroup
                        value={view}
                        exclusive
                        onChange={handleView}
                        aria-label="view"
                    >
                        <ToggleButton value="ph" aria-label="ph">
                            PH
                        </ToggleButton>
                        <ToggleButton value="fluo" aria-label="fluo">
                            FLUO
                        </ToggleButton>
                        <ToggleButton value="fluocontour" aria-label="fluocontour">
                            FLUO+Con.
                        </ToggleButton>
                        <ToggleButton value="fluox5" aria-label="fluox5">
                            FLUO x5
                        </ToggleButton>
                        <ToggleButton value="replot" aria-label="replot">
                            REPLOT
                        </ToggleButton>
                    </ToggleButtonGroup>
                </Stack>
                <br></br>
                <SquareImage imgSrc={imageUrl} size={400} />
            </Box>
        </div>
    );
}
