import React, { useEffect, useState, useRef } from 'react';
import { useParams } from 'react-router-dom';
import { Typography, Box, Grid, Link as MuiLink, CircularProgress } from '@mui/material';

interface Cell {
    cell_id: string;
}
interface Image {
    cellId: string;
    src: string;
}

interface ImageComponentProps {
    src: string;
    alt: string;
}

const useLazyLoad = (ref: React.RefObject<HTMLImageElement>, src: string): void => {
    useEffect(() => {
        const observer = new IntersectionObserver(([entry]) => {
            if (entry.isIntersecting) {
                if (ref.current) {
                    ref.current.src = src;
                }
                observer.disconnect();
            }
        });

        if (ref.current) {
            observer.observe(ref.current);
        }

        return () => observer.disconnect();
    }, [src]);
};

const ImageComponent: React.FC<ImageComponentProps> = ({ src, alt }) => {
    const imgRef = useRef<HTMLImageElement>(null);
    useLazyLoad(imgRef, src);

    return <img ref={imgRef} alt={alt} style={{ width: '100%' }} />;
};

const DbcontentsOverview: React.FC = () => {
    const { filename } = useParams<{ filename: string }>();
    const [cellImages, setCellImages] = useState<Image[]>([]);
    const [loading, setLoading] = useState<boolean>(false);

    useEffect(() => {
        const fetchImages = async () => {
            setLoading(true);
            try {
                const response = await fetch(`http://10.32.17.15:8000/cellapi/cells/databases/${filename}`);
                const cells: Cell[] = await response.json();

                const images: Image[] = await Promise.all(cells.map(async (cell: Cell) => {
                    const imageResponse = await fetch(`http://10.32.17.15:8000/cells/${filename}/overview/cell/${cell.cell_id}?draw_scale_bar=true`);
                    const imageData = await imageResponse.json();
                    return { cellId: cell.cell_id, src: `data:image/png;base64,${imageData.image}` };
                }));
                setCellImages(images);
            } catch (error) {
                console.error("Error fetching images: ", error);
            } finally {
                setLoading(false);
            }
        };

        fetchImages();
    }, [filename]);

    return (
        <Box marginX={2}>
            <Typography variant="h3" gutterBottom>
                {filename}
            </Typography>
            {loading ? (
                <Box display="flex" justifyContent="center" alignItems="center" height="100vh">
                    <CircularProgress />
                </Box>
            ) : (
                <Grid container spacing={2}>
                    {cellImages.map(({ cellId, src }) => (
                        <Grid item xs={2} key={cellId}>
                            <MuiLink href={`/dbcontents/${filename}/cell/${cellId.split('.')[0]}`}>
                                <ImageComponent src={src} alt={`Cell ${cellId}`} />
                            </MuiLink>
                        </Grid>
                    ))}
                </Grid>
            )}
        </Box>
    );
};

export default DbcontentsOverview;
