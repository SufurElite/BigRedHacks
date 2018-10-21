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
            MessageBoxButton button = MessageBoxButton.YesNoCancel;
           
            student_path = student_path.Replace(" ", "[").Replace("\\", "]");
            file_path = file_path.Replace(" ", "[").Replace("\\", "]");
            MessageBoxResult result3 = System.Windows.MessageBox.Show(file_path, "Confirm The Essay", button);
            start.Arguments = string.Format("{0} {1} {2}","main.py",file_path, student_path);
            start.UseShellExecute = false;
            start.RedirectStandardOutput = true;

            string result = "";
            using (Process process = Process.Start(start))
            {
                using (StreamReader reader = process.StandardOutput)
                {
                    result = reader.ReadToEnd();

                    MessageBoxResult result4 = System.Windows.MessageBox.Show(result, "Confirm The Essay", button);
                }
            }

        }
        private void Update_Stats(object sender, RoutedEventArgs e)
        {

        }
    }
    public class FileName
    {
        public string Name { get; set; }
    }
}
