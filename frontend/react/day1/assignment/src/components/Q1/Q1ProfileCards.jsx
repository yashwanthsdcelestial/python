import React from "react";
import ProfileCard from "./ProfileCard";

const profiles = [
  {
    name: "Rahul",
    title: "Frontend Developer",
    bio: "Passionate about building beautiful UIs and great user experiences.",
    avatarUrl: "https://i.pravatar.cc/150?img=1",
  },
  {
    name: "Rocky",
    title: "Backend Engineer",
    bio: "Loves scalable systems, clean APIs, and strong coffee.",
    avatarUrl: "https://i.pravatar.cc/150?img=3",
  },
  {
    name: "Raya",
    title: "UI/UX Designer",
    bio: "Turning complex problems into delightful digital experiences.",
    avatarUrl: "https://i.pravatar.cc/150?img=5",
  },
];

function Q1ProfileCards() {
  return (
    <div>
      <h2>Q1 — Personal Profile Cards</h2>
      <div style={{ display: "flex", gap: "24px", flexWrap: "wrap" }}>
        {profiles.map((p) => (
          <ProfileCard key={p.name} {...p} />
        ))}
      </div>
    </div>
  );
}

export default Q1ProfileCards;
