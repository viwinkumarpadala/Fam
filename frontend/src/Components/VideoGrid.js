

import React, { useState, useEffect } from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faArrowRight, faArrowLeftLong, faBackward, faForward } from '@fortawesome/free-solid-svg-icons';
import './Video.css';

const VideoGrid = ({ videos }) => {
  const [currentPage, setCurrentPage] = useState(1);
  const itemsPerPage = 8;

  useEffect(() => {
    setCurrentPage(1); // Reset page number when videos change
  }, [videos]);

  const totalVideos = videos.length;
  const indexOfLastVideo = currentPage * itemsPerPage;
  const indexOfFirstVideo = indexOfLastVideo - itemsPerPage;
  const currentVideos = videos.slice(indexOfFirstVideo, indexOfLastVideo);

  const handlePagination = (page) => {
    setCurrentPage(page);
  };

  const generatePageNumbers = () => {
    return Array.from({ length: Math.ceil(totalVideos / itemsPerPage) }, (_, index) => index + 1);
  };

  return (
    <>
      <div className="video-grid">
        {currentVideos.map(video => (
          <div key={video._id} className="video-card" onClick={() => handleClick(video.videoId)}>
            <img src={video.thumbnail} alt={video.title} />
            <h3>{video.title}</h3>
            <p>{video.description}</p>
            <p>{video.publishedAt}</p>
          </div>
        ))}
      </div>
      <div className="pagination">
        <button className='pagi' onClick={() => handlePagination(1)}>
          <FontAwesomeIcon icon={faBackward} /> First</button>
        <button className='pagi' onClick={() => handlePagination(currentPage > 1 ? currentPage - 1 : 1)}>
          <FontAwesomeIcon icon={faArrowLeftLong} /> Prev
        </button>
        {generatePageNumbers().map((page) => (
          <button
            key={page}
            className={page === currentPage ? 'active' : ''}
            onClick={() => handlePagination(page)}
          >
            {page}
          </button>
        ))}
        <button className='pagi'
          onClick={() =>
            handlePagination(
              currentPage < Math.ceil(totalVideos / itemsPerPage)
                ? currentPage + 1
                : currentPage
            )
          }
        >
          Next <FontAwesomeIcon icon={faArrowRight} />
        </button>
        <button className='pagi'
          onClick={() =>
            handlePagination(Math.ceil(totalVideos / itemsPerPage))
          }
        >
          Last <FontAwesomeIcon icon={faForward} />
        </button>
      </div>
    </>
  );
};

const handleClick = (videoId) => {
  // Redirect to the selected video page
  window.location.href = `https://www.youtube.com/watch?v=${videoId}`;
}

export default VideoGrid;
