import { useEffect, useState } from "react";

export default function Dashboard() {
  const [message, setMessage] = useState("");

  useEffect(() => {
    const socket = new WebSocket("wss://a3mongo.onrender.com/ws");
    socket.onmessage = (event) => setMessage(event.data);
  }, []);

  return <div>Mensagem em tempo real: {message}</div>;
}
