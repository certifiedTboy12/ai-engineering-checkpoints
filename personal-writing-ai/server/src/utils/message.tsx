export function messageFormat(sender: string, text?: string, type?: string) {
  return {
    sender,
    text,
    type,
  };
}
