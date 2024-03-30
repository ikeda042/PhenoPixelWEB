import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { Typography, Box, Grid } from '@mui/material';
interface Cell {
    cell_id: number;
}


export default function DbcontentsOverview() {
    const { filename } = useParams();
    const [cellImages, setCellImages] = useState([]);

    useEffect(() => {
        const fetchImages = async () => {
            try {
                const response = await fetch(`http://10.32.17.15:8000/cellapi/cells/databases/${filename}`);
                const cells = await response.json();

                const images = await Promise.all(cells.map(async (cell: Cell) => {
                    const imageResponse = await fetch(`http://10.32.17.15:8000/cellapi/cells/${filename}/cell/${cell.cell_id}/overview`);
                    const imageData = await imageResponse.json();
                    return { cellId: cell.cell_id, src: `data:image/png;base64,${imageData.image}` };
                }));
                setCellImages(images);
            } catch (error) {
                console.error("Error fetching images: ", error);
            }
        };

        fetchImages();
    }, [filename]);

    return (
        <Box>
            <Typography variant="h3" gutterBottom>
                {filename}
            </Typography>
            <Grid container spacing={2}>
                {cellImages.map(({ cellId, src }) => (
                    <Grid item xs={12} sm={6} md={4} key={cellId}>
                        <img src={src} alt={`Cell ${cellId}`} style={{ width: '100%' }} />
                    </Grid>
                ))}
            </Grid>
        </Box>
    );
}
