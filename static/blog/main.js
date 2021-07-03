const canvas = document.getElementById("canvas");
const ctx = canvas.getContext("2d");

let img = new Image();
let fileName = "";

const downloadBtn = document.getElementById("download-btn");
const uploadFile = document.getElementById("upload-file");
const revertBtn = document.getElementById("revert-btn");


// Filter & Effect Handlers
document.addEventListener("click", e => {
  if (e.target.classList.contains("filter-btn")) {
    if (e.target.classList.contains("brightness-add")) {
      Caman("#canvas", img, function() {
        this.brightness(5).render();
      });
    } else if (e.target.classList.contains("brightness-remove")) {
      Caman("#canvas", img, function() {
        this.brightness(-5).render();
      });
    } else if (e.target.classList.contains("contrast-add")) {
      Caman("#canvas", img, function() {
        this.contrast(5).render();
      });
    } else if (e.target.classList.contains("contrast-remove")) {
      Caman("#canvas", img, function() {
        this.contrast(-5).render();
      });
    } else if (e.target.classList.contains("saturation-add")) {
      Caman("#canvas", img, function() {
        this.saturation(5).render();
      });
    } else if (e.target.classList.contains("saturation-remove")) {
      Caman("#canvas", img, function() {
        this.saturation(-5).render();
      });
    } else if (e.target.classList.contains("vibrance-add")) {
      Caman("#canvas", img, function() {
        this.vibrance(5).render();
      });
    } else if (e.target.classList.contains("vibrance-remove")) {
      Caman("#canvas", img, function() {
        this.vibrance(-5).render();
      });
    } else if (e.target.classList.contains("gamma-add")) {
      Caman("#canvas", img, function() {
        this.gamma(0.5).render();
      });
    } else if (e.target.classList.contains("rev-gamma-add")) {
      Caman("#canvas", img, function() {
        this.gamma(1.4).render();
      });
    } else if (e.target.classList.contains("Exposure-add")) {
      Caman("#canvas", img, function() {
        this.exposure(3).render();
      });
    } else if (e.target.classList.contains("Exposure-remove")) {
      Caman("#canvas", img, function() {
        this.exposure(-3).render();
      });
    } else if (e.target.classList.contains("noise-add")) {
      Caman("#canvas", img, function() {
        this.noise(3).render();
      });
    } else if (e.target.classList.contains("clip-add")) {
      Caman("#canvas", img, function() {
        this.clip(20).render();
      });
    } else if (e.target.classList.contains("Hue-add")) {
      Caman("#canvas", img, function() {
        this.hue(5).render();
      });
    } else if (e.target.classList.contains("sepia-add")) {
      Caman("#canvas", img, function() {
        this.sepia(5).render();
      });
    } else if (e.target.classList.contains("SHARPEN-add")) {
      Caman("#canvas", img, function() {
        this.sharpen(5).render();
      });
    } else if (e.target.classList.contains("StackBlur-add")) {
      Caman("#canvas", img, function() {
        this.stackBlur(5).render();
      });
    } else if (e.target.classList.contains("profile-add")) {
      Caman("#canvas", img, function() {
        this.tiltShift({
            angle: 90,
            focusWidth: 600
        }).render();
      });
    } else if (e.target.classList.contains("vintage-add")) {
      Caman("#canvas", img, function() {
        this.vintage().render(function () {
            alert("Done!");
        });
      });
    } else if (e.target.classList.contains("lomo-add")) {
      Caman("#canvas", img, function() {
        this.lomo().render(function () {
            alert("Done!");
        });
      });
    } else if (e.target.classList.contains("clarity-add")) {
      Caman("#canvas", img, function() {
        this.clarity().render(function () {
            alert("Done!");
        });
      });
    } else if (e.target.classList.contains("sincity-add")) {
      Caman("#canvas", img, function() {
        this.sinCity().render(function () {
            alert("Done!");
        });
      });
    } else if (e.target.classList.contains("hazy-add")) {
      Caman("#canvas", img, function() {
        this.hazyDays().render(function () {
            alert("Done!");
        });
      });
    } else if (e.target.classList.contains("crossprocess-add")) {
      Caman("#canvas", img, function() {
        this.crossProcess().render(function () {
            alert("Done!");
        });
      });
    } else if (e.target.classList.contains("pinhole-add")) {
      Caman("#canvas", img, function() {
        this.pinhole().render(function () {
            alert("Done!");
        });
      });
    } else if (e.target.classList.contains("nostalgia-add")) {
      Caman("#canvas", img, function() {
        this.nostalgia().render(function () {
            alert("Done!");
        });
      });
    } else if (e.target.classList.contains("hermajesty-add")) {
      Caman("#canvas", img, function() {
        this.herMajesty().render(function () {
            alert("Done!");
        });
      });
    } else if (e.target.classList.contains("grungy-add")) {
      Caman("#canvas", img, function() {
        this.grungy().render(function () {
            alert("Done!");
        });
      });
    } else if (e.target.classList.contains("radial-add")) {
      Caman("#canvas", img, function() {
        this.radialBlur().render(function () {
            alert("Done!");
        });
      });
    } else if (e.target.classList.contains("jackas-add")) {
      Caman("#canvas", img, function() {
        this.jarques().render(function () {
            alert("Done!");
          });
      });
    }
  }
});

// Revert Filters
revertBtn.addEventListener("click", e => {
  Caman("#canvas", img, function() {
    this.revert();
  });
});

// Upload File
uploadFile.addEventListener("change", () => {
  // Get File
  const file = document.getElementById("upload-file").files[0];
  // Init FileReader API
  const reader = new FileReader();

  // Check for file
  if (file) {
    // Set file name
    fileName = file.name;
    // Read data as URL
    reader.readAsDataURL(file);
  }

  // Add image to canvas
  reader.addEventListener(
    "load",
    () => {
      // Create image
      img = new Image();
      // Set image src
      img.src = reader.result;
      // On image load add to canvas
      img.onload = function() {
        canvas.width = img.width;
        canvas.height = img.height;
        ctx.drawImage(img, 0, 0, img.width, img.height);
        canvas.removeAttribute("data-caman-id");
      };
    },
    false
  );
});

// Download Event
downloadBtn.addEventListener("click", () => {
  // Get ext
  const fileExtension = fileName.slice(-4);

  // Init new filename
  let newFilename;

  // Check image type
  if (fileExtension === ".jpg" || fileExtension === ".png") {
    // new filename
    newFilename = fileName.substring(0, fileName.length - 4) + "-edited.jpg";
  }

  // Call download
  download(canvas, newFilename);
});

// Download
function download(canvas, filename) {
  // Init event
  let e;
  // Create link
  const link = document.createElement("a");

  // Set props
  link.download = filename;
  link.href = canvas.toDataURL("image/jpeg", 0.8);
  // New mouse event
  e = new MouseEvent("click");
  // Dispatch event
  link.dispatchEvent(e);
}