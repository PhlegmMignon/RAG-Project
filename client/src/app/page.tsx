import ChatHistory from "@/components/ChatHistory";
import InputBox from "../components/InputBox";

const Home: React.FC = () => {
  return (
    <div className="flex flex-col w-full overflow-auto">
      <ChatHistory />
      <InputBox />
    </div>
  );
};

export default Home;
