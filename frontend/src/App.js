import React, { useState, useEffect } from 'react';
import Logo from './Components/Logo';
import SearchBar from './Components/SearchBar';
import VideoGrid from './Components/VideoGrid';
import './App.css';

function App() {
  // State variables
  const [videos, setVideos] = useState([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [cachedVideosFetched, setCachedVideosFetched] = useState(false);

  // useEffect to fetch cached videos when the component mounts
  useEffect(() => {
    fetchCachedVideos();
  }, []);

  // Function to fetch cached videos
  const fetchCachedVideos = async () => {
    try {
      const response = await fetch('http://127.0.0.1:5000/videos/cached');
      if (response.ok) {
        const data = await response.json();
        setVideos(data.videos);
        setCachedVideosFetched(true); 
        console.log(videos)
      } else {
        throw new Error('Failed to fetch cached videos');
      }
    } catch (error) {
      console.error('Error fetching cached videos:', error); 
    }
  };

  // Function to search videos based on query
  const searchVideos = async (query) => {
    try {
      const response = await fetch(`http://127.0.0.1:5000/videos?query=${query}`);
      if (response.ok) {
        const data = await response.json();
        setVideos(data.videos);
      } else {
        throw new Error('Failed to search videos');
      }
    } catch (error) {
      console.error('Error searching videos:', error);
    }
  };

  // Function to handle search
  const handleSearch = async (term) => {
    setSearchTerm(term);
    await searchVideos(term);
  };

  return (
    <div className="App">
      {/* Logo component */}
      <Logo />

      {/* SearchBar component with handleSearch as prop */}
      <SearchBar onSearch={handleSearch} />

      {/* Button to fetch cached videos */}
      {/* <button onClick={() => fetchCachedVideos()} disabled={!cachedVideosFetched}>
        Fetch Cached Videos
      </button> */}

      {/* VideoGrid component to display videos */}
      <br />
      <br />
      <VideoGrid videos={videos} />
    </div>
  );
}

export default App;
