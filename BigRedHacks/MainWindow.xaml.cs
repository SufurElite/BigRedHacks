using Microsoft.Win32;
using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Forms;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Navigation;
using System.Windows.Shapes;
using System.Collections.ObjectModel;
using System.Diagnostics;

namespace BigRedHacks
{
    
    public partial class MainWindow : Window
    {
        string student_path;
        string file_path;
        List<FileName> files2;
        public MainWindow()
        {
            InitializeComponent();
        }

        private void Select_Student(object sender, RoutedEventArgs e)
        {
            using (var dialog = new System.Windows.Forms.FolderBrowserDialog())
            {
                dialog.SelectedPath = Directory.GetCurrentDirectory();
                System.Windows.Forms.DialogResult result = dialog.ShowDialog();
                student_path = dialog.SelectedPath;
            }
            
            DirectoryInfo d = new DirectoryInfo(student_path);//Assuming Test is your Folder
            FileInfo[] Files = d.GetFiles("*.txt"); //Getting Text files

            files2 = new List<FileName>();
            ListView1.ItemsSource = files2;
            foreach (FileInfo file in Files)
            {
                files2.Add(new FileName { Name = file.Name}); 
            }
            ListView1.ItemsSource = files2;

        }
        private void Select_Essay(object sender, RoutedEventArgs e)
        {
            using (var dialog = new System.Windows.Forms.OpenFileDialog())
            {
                dialog.InitialDirectory = Directory.GetCurrentDirectory();
                dialog.Filter = "Text Files (*.txt)|";
                dialog.DefaultExt = ".txt";
                dialog.ShowDialog();
                file_path = dialog.FileName;
            }
            MessageBoxButton button = MessageBoxButton.YesNoCancel;
            MessageBoxResult result = System.Windows.MessageBox.Show(file_path, "Confirm The Essay", button);
            
        }
        private void Run_Model(object sender, RoutedEventArgs e)
        {
            ProcessStartInfo start = new ProcessStartInfo();
            start.FileName = "python.exe";
            
            string student_path2 = student_path.Replace(" ", "[").Replace("\\", "]");
            string file_path2 = file_path.Replace(" ", "[").Replace("\\", "]");
            start.Arguments = string.Format("{0} {1} {2}","main.py", file_path2, student_path2);
            start.UseShellExecute = false;
            start.RedirectStandardOutput = true;
            string result = "";
            using (Process process = Process.Start(start))
            {
                using (StreamReader reader = process.StandardOutput)
                {
                    result = reader.ReadToEnd();
                }
            }
            Probability.Text = "Plagarism Probability: " + float.Parse(result,System.Globalization.CultureInfo.InvariantCulture)*100+"%";

        }
        private void Update_Stats(object sender, RoutedEventArgs e)
        {
            if (file_path != "" && student_path != "")
            {
                string fileName = System.IO.Path.GetFileName(file_path);
                string sourcePath = System.IO.Path.GetDirectoryName(file_path);
                string targetPath = student_path;

                // Use Path class to manipulate file and directory paths.
                string sourceFile = System.IO.Path.Combine(sourcePath, fileName);
                string destFile = System.IO.Path.Combine(targetPath, fileName);

                System.IO.File.Copy(sourceFile, destFile, true);

                fileName = System.IO.Path.GetFileName(file_path);
                destFile = System.IO.Path.Combine(targetPath, fileName);
                System.IO.File.Copy(file_path, destFile, true);

                ProcessStartInfo start = new ProcessStartInfo();
                start.FileName = "python.exe";

                start.Arguments = string.Format("{0}", "main.py");
                start.UseShellExecute = false;
                start.RedirectStandardOutput = true;
                Process.Start(start);
            }
        }
    }
    public class FileName
    {
        public string Name { get; set; }
    }
}
