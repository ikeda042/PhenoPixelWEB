
import { DataGrid, GridColDef, GridRenderCellParams, } from '@mui/x-data-grid';
import { Typography } from '@mui/material';
import { useParams } from 'react-router-dom';
import { useEffect, useState } from 'react';
import { Button } from '@mui/material';
import { Box } from '@mui/system';
import Grid from '@mui/material/Unstable_Grid2';
import Link from '@mui/material/Link';

export default function DbcontentsOverview() {
    const { filename } = useParams();
    const [cellIds, setCellIds] = useState<string[]>([]);

    // class CellDB(BaseModel):
    //     cell_id: str
    //     label_experiment: str
    //     manual_label: int
    //     perimeter: float
    //     area: float

    // @router_cell.get("/cells/databases/{db_name}", response_model=list[CellDB])
    //     async def read_cell_db(db_name: str):
    //         print(db_name)
    //         print(f"./databases/{db_name}++++++++++++++++++++++++++++++++++++++")
    //         return await get_cells(f"./databases/{db_name}.db")

    // @router_cell.get("/cells/{db_name}/cell/{cell_id}/fluox5")
    // async def read_cell_fluo5(db_name: str, cell_id: str,draw_scale_bar: bool = Query(default=True)):
    //     cell: bytes = await get_cell_fluo(f"./databases/{db_name}.db", cell_id)
    //     image_fluo = cv2.imdecode(np.frombuffer(cell, dtype=np.uint8), cv2.IMREAD_COLOR)
    //     image_fluo = cv2.convertScaleAbs(image_fluo, alpha=5, beta=0)
    //     if draw_scale_bar:
    //         image_fluo = await draw_scale_bar_with_centered_text(image_fluo)
    //     _, buffer = cv2.imencode(".png", image_fluo)
    //     async with aiofiles.open("temp_fluo5.png", "wb") as afp:
    //         await afp.write(buffer)
    //     return StreamingResponse(open("temp_fluo5.png", "rb"), media_type="image/png")

    useEffect(() => {
        const fetchData = async () => {
            try {
                const response = await fetch(`http://10.32.17.15:8000/cellapi/cells/databases/${filename}`);
                const data = await response.json();
                const cellIds = data.map((cell: any) => cell.cell_id);  // Extract cell_id from each item
                setCellIds(cellIds);
            } catch (error) {
                console.error("Error fetching data: ", error);
            }
        };

        fetchData();
    }, [filename]);

    return (
        <Box>
            <Typography variant="h3" gutterBottom>
                {filename}
            </Typography>
            <Grid container spacing={4}>
                {cellIds.map((cellId) => (
                    <Grid key={cellId}>
                        <Link href={`/dbcontents/${filename}/cell/${cellId}`}>{cellId}</Link>
                    </Grid>
                ))}
            </Grid>
        </Box>
    );




};
