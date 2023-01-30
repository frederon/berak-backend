export const loadFile = (
  info: any,
  callback: React.Dispatch<React.SetStateAction<string>>,
  error_callback: (text: string) => void
) => {
  const reader = new FileReader();
  reader.onload = function (event) {
    if (event && event.target && event.target.result) {
      const result = event.target.result as string
      callback(result)
    } else {
      error_callback("An error occured when reading the file")
    }
  };

  reader.readAsText(info.file.originFileObj)
}

export const saveFile = function (data: any, fileName: string) {
  const blob = new Blob([data], { type: "text/plain" });
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.download = fileName;
  link.href = url;
  link.click();
}

export const toUppercaseAndFilterAlphabets = (text: string): string => {
  return text
    .toUpperCase()
    .split('')
    .filter(char => /[A-Z]/.test(char))
    .join('')
}

export const spacesEvery5Chars = (text: string,): string => {
  return toUppercaseAndFilterAlphabets(text).match(/.{5}/g)!.join(' ');
}