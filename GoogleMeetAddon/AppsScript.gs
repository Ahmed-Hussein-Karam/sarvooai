function doGet(e) {
  return HtmlService.createHtmlOutputFromFile('Index')
    .setTitle('Interview Transcripts Add-on');
}

function extractTextFromCv(fileContent) {
  try {
    var decodedContent = Utilities.base64Decode(fileContent); // Decode base64 content
    var text = Utilities.newBlob(decodedContent).getDataAsString(); // Convert Blob to text

    return text;
  } catch (error) {
    console.error('Error extracting text from TXT:', error);
    return 'Error extracting text from TXT. Please try again.';
  }
}

function fetchTranscript() {
  // Due to API limitations, use sample interview data
  var interviewScripts = [
    "Interview Transcript 1: Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
    "Interview Transcript 2: Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.",
    "Interview Transcript 3: Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris."
  ];

  // Select a random index from the interviewScripts array
  var randomIndex = Math.floor(Math.random() * interviewScripts.length);
  var transcriptText = interviewScripts[randomIndex];

  return transcriptText;
}