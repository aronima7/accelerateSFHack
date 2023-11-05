import londonImage from './london.png';

const AvatarLondon = () => {
  return (
    <div className="relative w-10 h-10 overflow-hidden bg-gray-100 rounded-full">
      <img
        src={londonImage}
        alt="AvatarLondon"
        className="absolute w-full h-full object-cover"
      />
    </div>
  );
};

export default AvatarLondon;
