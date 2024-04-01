
import * as React from 'react';
import { useParams } from 'react-router-dom';
import { useEffect, useState } from 'react';
import { Button } from '@mui/material';
import { Box } from '@mui/system';
import SquareImage from '../components/Squareimage';
import { ToggleButton, ToggleButtonGroup } from '@mui/material';
import { Stack } from '@mui/material';
import { FormControlLabel, Checkbox } from '@mui/material';
import { Table, TableBody, TableCell, TableContainer, TableRow } from '@mui/material';
import { useNavigate } from 'react-router-dom';




type CellStats = {
    basic_cell_info: {
        cell_id: string,
        label_experiment: string,
        manual_label: number,
        perimeter: number,
        area: number
    },
    max_brightness: number,
    min_brightness: number,
    mean_brightness_raw: number,
    mean_brightness_normalized: number,
    median_brightness_raw: number,
    median_brightness_normalized: number,
    ph_max_brightness?: number | null,
    ph_min_brightness?: number | null,
    ph_mean_brightness_raw?: number | null,
    ph_mean_brightness_normalized?: number | null,
    ph_median_brightness_raw?: number | null,
    ph_median_brightness_normalized?: number | null
};

export default function Cell() {
    const { filename, cellId } = useParams<{ filename: string, cellId: string }>();
    const [view, setView] = useState('ph');
    const [scalebar, setScalebar] = useState(false);
    const [cellStats, setCellStats] = useState<CellStats | null>(null);
    const navigate = useNavigate();


    const handleView = (event: React.MouseEvent<HTMLElement>, newView: string) => {
        setView(newView);
    };

    const handleScalebarChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        setScalebar(event.target.checked);
    };

    useEffect(() => {
        fetch(`http://10.32.17.15:8000/cellapi/cells/${filename}/cells/${cellId}/stats`)
            .then(response => response.json())
            .then(data => setCellStats(data));
    }, [filename, cellId]);


    const imageUrl = `http://10.32.17.15:8000/cellapi/cells/${filename}/cell/${cellId}/${view}?draw_scale_bar=${scalebar}`;

    return (
        <div style={{ height: 700, width: '100%' }}>

            <Box sx={{ display: 'flex', flexDirection: 'column-reverse', justifyContent: 'center', alignItems: 'center', height: '80vh' }}>
                <Stack direction="row" spacing={3} alignItems="center">
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
                    <Button
                        variant="contained"
                        style={{
                            backgroundColor: 'black',
                            color: 'white',
                            height: '40px'
                        }}

                        href={imageUrl}
                        download
                    >
                        Export Image
                    </Button>
                </Stack>
                <br></br>
                <Box sx={{ display: 'flex', flexDirection: 'row', justifyContent: 'center', alignItems: 'center', height: '80vh' }}>
                    <SquareImage imgSrc={imageUrl} size={500} />
                    <Box sx={{ marginLeft: 2 }}>
                        <TableContainer>
                            <Table>
                                <TableBody>
                                    <TableRow>
                                        <TableCell>表示モード</TableCell>
                                        <TableCell align='center'>{view}</TableCell>
                                    </TableRow>

                                    <TableRow>
                                        <TableCell >Database / Cell ID</TableCell>
                                        <TableCell align='center'>{filename} / {cellId}</TableCell>
                                    </TableRow>
                                    <TableRow>
                                        <TableCell >周囲長 (px) / 面積 (px^2)</TableCell>
                                        <TableCell align='center'>{cellStats?.basic_cell_info.perimeter} / {cellStats?.basic_cell_info.area}</TableCell>
                                    </TableRow>

                                    {view === 'ph' || view === 'phcontour' ? (
                                        <>
                                            <TableRow>
                                                <TableCell >最大位相差輝度</TableCell>
                                                <TableCell align='center'>{cellStats?.ph_max_brightness}</TableCell>
                                            </TableRow>
                                            <TableRow>
                                                <TableCell>最小位相差輝度</TableCell>
                                                <TableCell align='center'>{cellStats?.ph_min_brightness}</TableCell>
                                            </TableRow>
                                            <TableRow>
                                                <TableCell>平均位相差輝度(8bit)</TableCell>
                                                <TableCell align='center'>{cellStats?.ph_mean_brightness_raw}</TableCell>
                                            </TableRow>
                                            <TableRow>
                                                <TableCell>中央値位相差輝度(8bit)</TableCell>
                                                <TableCell align='center'>{cellStats?.ph_median_brightness_raw}</TableCell>
                                            </TableRow>
                                            <TableRow>
                                                <TableCell>平均位相差輝度(正規化)</TableCell>
                                                <TableCell align='center'>{cellStats?.ph_mean_brightness_normalized}</TableCell>
                                            </TableRow>
                                            <TableRow>
                                                <TableCell>中央値位相差輝度(正規化)</TableCell>
                                                <TableCell align='center'>{cellStats?.ph_median_brightness_normalized}</TableCell>
                                            </TableRow>
                                        </>
                                    ) : (
                                        <>
                                            <TableRow>
                                                <TableCell>最大蛍光輝度(8bit)</TableCell>
                                                <TableCell align='center'>{cellStats?.max_brightness}</TableCell>
                                            </TableRow>
                                            <TableRow>
                                                <TableCell>最小蛍光輝度(8bit)</TableCell>
                                                <TableCell align='center'>{cellStats?.min_brightness}</TableCell>
                                            </TableRow>
                                            <TableRow>
                                                <TableCell>平均蛍光輝度(8bit)</TableCell>
                                                <TableCell align='center'>{cellStats?.mean_brightness_raw}</TableCell>
                                            </TableRow>
                                            <TableRow>
                                                <TableCell>中央値蛍光輝度(8bit)</TableCell>
                                                <TableCell align='center'>{cellStats?.median_brightness_raw}</TableCell>
                                            </TableRow>
                                            <TableRow>
                                                <TableCell>平均蛍光輝度(正規化)</TableCell>
                                                <TableCell align='center'>{cellStats?.mean_brightness_normalized}</TableCell>
                                            </TableRow>
                                            <TableRow>
                                                <TableCell>中央値蛍光輝度(正規化)</TableCell>
                                                <TableCell align='center'>{cellStats?.median_brightness_normalized}</TableCell>
                                            </TableRow>
                                        </>
                                    )}
                                </TableBody>
                            </Table>
                        </TableContainer>

                    </Box>
                </Box>
            </Box>
        </div >
    );
}
