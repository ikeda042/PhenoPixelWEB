
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
import { FormControlLabel, Checkbox } from '@mui/material';

export default function Cell() {
    const { filename, cellId } = useParams<{ filename: string, cellId: string }>();
    const [view, setView] = useState('ph');
    const [scalebar, setScalebar] = useState(false);

    const handleView = (event: React.MouseEvent<HTMLElement>, newView: string) => {
        setView(newView);
    };

    const handleScalebarChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        setScalebar(event.target.checked);
    };

    const imageUrl = `http://10.32.17.15:8000/cellapi/cells/${filename}/cell/${cellId}/${view}?draw_scale_bar=${scalebar}`;

    return (
        <div style={{ height: 700, width: '100%' }}>
            <Typography variant="h6" align="center" gutterBottom>
                Cell ID: {cellId} ({filename})
            </Typography>
            <Box sx={{ display: 'flex', flexDirection: 'column-reverse', justifyContent: 'center', alignItems: 'center', height: '80vh' }}>
                <Stack direction="row" spacing={3}>
                    <ToggleButtonGroup
                        value={view}
                        exclusive
                        onChange={handleView}
                        aria-label="view"
                        size='large'
                    >
                        <ToggleButton value="ph" aria-label="ph">
                            PH
                        </ToggleButton>
                        <ToggleButton value="fluo" aria-label="fluo">
                            FLUO
                        </ToggleButton>
                        <ToggleButton value="phcontour" aria-label="phcontour">
                            PH + Con.
                        </ToggleButton>
                        <ToggleButton value="fluocontour" aria-label="fluocontour">
                            FLUO+Con.
                        </ToggleButton>
                        <ToggleButton value="fluox5" aria-label="fluox5">
                            FLUO x5
                        </ToggleButton>
                        <ToggleButton value="fluohadamard" aria-label="fluohadamard">
                            FLUO MASKed
                        </ToggleButton>
                        <ToggleButton value="replot" aria-label="replot">
                            REPLOT
                        </ToggleButton>
                    </ToggleButtonGroup>
                    <FormControlLabel
                        control={<Checkbox checked={scalebar} onChange={handleScalebarChange} />}
                        label="Scalebar"
                    />
                    <Button variant="contained" style={{ backgroundColor: 'black', color: 'white' }} href={imageUrl} download>
                        Export Image
                    </Button>
                </Stack>
                <br></br>
                <Box sx={{ display: 'flex', flexDirection: 'row', justifyContent: 'center', alignItems: 'center', height: '80vh' }}>
                    <SquareImage imgSrc={imageUrl} size={500} />
                    <Box sx={{ marginLeft: 2 }}>
                        <Typography variant="h5">
                            Stats:
                        </Typography>
                        <Typography variant="body1">
                            細胞の統計情報1
                        </Typography>
                        <Typography variant="body1">
                            細胞の統計情報2
                        </Typography>
                        <Typography variant="body1">
                            細胞の統計情報3
                        </Typography>
                    </Box>
                </Box>
            </Box>
        </div>
    );
}
