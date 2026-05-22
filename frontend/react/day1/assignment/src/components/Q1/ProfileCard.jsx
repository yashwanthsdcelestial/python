import React from "react";
import "./ProfileCard.css";

function ProfileCard({ name, title, bio, avatarUrl }) {
  return (
    <div className="profile-card">
      <img src={avatarUrl} alt={name} className="profile-avatar" />
      <h2 className="profile-name">{name}</h2>
      <p className="profile-title">{title}</p>
      <p className="profile-bio">{bio}</p>
    </div>
  );
}

export default ProfileCard;
