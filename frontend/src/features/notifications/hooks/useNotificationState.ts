import { useState } from 'react';
export function useNotificationState() {
  const [items, setItems] = useState([]);
  return { items, unreadCount: 0 };
}
