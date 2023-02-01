export const loadFile = (
  info: any,
  callback: React.Dispatch<React.SetStateAction<string>> | React.Dispatch<React.SetStateAction<ArrayBuffer>>,
  error_callback: (text: string) => void,
  isBytes: boolean = false
) => {
  const reader = new FileReader();
  reader.onload = function (event) {
    if (event && event.target && event.target.result) {
      const result = event.target.result
      console.log(result)
      console.log(typeof (result))
      // @ts-ignore
      callback(result)
    } else {
      error_callback("An error occured when reading the file")
    }
  };

  if (isBytes) {
    reader.readAsArrayBuffer(info.file.originFileObj)
  } else {
    reader.readAsText(info.file.originFileObj)
  }
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
  return toUppercaseAndFilterAlphabets(text).match(/.{1,5}/g)!.join(' ');
}