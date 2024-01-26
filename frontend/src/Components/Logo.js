import React from 'react';

const Logo = () => {
  const headingStyle = {
    fontSize: '48px',
    fontWeight: 'bold',
    color: '#333', 
    textTransform: 'uppercase',
    margin: '20px 0',
    textAlign: 'center'
  };

  return (
    <div className="logo">
      <h1 style={headingStyle}>UTube</h1>
    </div>
  );
};

export default Logo;
