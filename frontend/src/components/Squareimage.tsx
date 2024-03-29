import React from 'react';

interface SquareImageProps {
    imgSrc: string;
    size: number;
}

const SquareImage: React.FC<SquareImageProps> = ({ imgSrc, size }) => {
    return (
        <div style={{
            width: size,
            height: size,
            backgroundImage: `url(${imgSrc})`,
            backgroundSize: 'cover',
            backgroundPosition: 'center',
        }} />
    );
}

export default SquareImage;
