import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { Typography, Box, Grid, Link as MuiLink } from '@mui/material';

interface Cell {
    cell_id: string;
}
interface Image {
    cellId: string;
    src: string;
}

export default function DbcontentsOverview() {
    const { filename } = useParams();
    const [cellImages, setCellImages] = useState<Image[]>([]);

    useEffect(() => {
        const fetchImages = async () => {
            try {
                const response = await fetch(`http://10.32.17.15:8000/cellapi/cells/databases/${filename}`);
                const cells = await response.json();

                const images: Image[] = await Promise.all(cells.map(async (cell: Cell) => {
                    const imageResponse = await fetch(`http://10.32.17.15:8000/cells/${filename}/overview/cell/${cell.cell_id}?draw_scale_bar=true`);
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
        <Box marginX={2}>
            <Typography variant="h3" gutterBottom>
                {filename}
            </Typography>
            <Grid container spacing={2}>
                {cellImages.map(({ cellId, src }) => (
                    <Grid item xs={2} key={cellId}>
                        <MuiLink href={`/dbcontents/${filename}/cell/${cellId.split('.')[0]}`}>
                            <img src={src} alt={`Cell ${cellId}`} style={{ width: '100%' }} />
                        </MuiLink>
                    </Grid>
                ))}
            </Grid>
        </Box>
    );
}
